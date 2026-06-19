// Hybrid Database Bridge (Firebase Cloud / Android SQLite / LocalStorage Fallback)
// Exposes a unified API for Products, Cart, Orders, and Auth.
// CRITICAL: The fetch interceptor is installed SYNCHRONOUSLY at the top
// to ensure it catches /cart/add requests even before Firebase loads.

// ============================================================
// 1. INSTALL FETCH INTERCEPTOR IMMEDIATELY (synchronous)
// ============================================================

const originalFetch = window.fetch;

const isFlattened = window.location.pathname.indexOf('full%20download') !== -1 || 
                    window.location.pathname.indexOf('full download') !== -1 ||
                    window.location.pathname.indexOf('downloaded_site') !== -1 ||
                    window.location.pathname.indexOf('android_asset') !== -1 ||
                    window.location.pathname.indexOf('products_') !== -1 ||
                    window.location.pathname.indexOf('pages_') !== -1;

const folderSeparator = isFlattened ? 'products_' : 'products/';
const fileSuffix = isFlattened ? '/index.html' : '/';

function isDummyBundleProduct(item) {
  if (!item) return false;
  const name = (item.name || item.title || '').toLowerCase();
  const slug = (item.slug || item.productId || '').toLowerCase();
  const id = String(item.id || '').toLowerCase();
  return name.indexOf('build your bundle') !== -1 || 
         name.indexOf('choose any 3') !== -1 ||
         slug.indexOf('build-your-bundle') !== -1 ||
         id.indexOf('build-your-bundle') !== -1;
}

// LocalStorage-only cart for the interceptor (works without Firebase)
function _getLocalCart() {
  try {
    const data = localStorage.getItem('rawjoy_cart_hybrid') || '{"items":[]}';
    const parsed = JSON.parse(data);
    
    // Filter out dummy/virtual bundle products
    const filteredItems = [];
    for (let i = 0; i < parsed.items.length; i++) {
      const item = parsed.items[i];
      if (!isDummyBundleProduct(item)) {
        filteredItems.push(item);
      }
    }
    parsed.items = filteredItems;
    
    let total = 0;
    for (let i = 0; i < parsed.items.length; i++) {
      const item = parsed.items[i];
      let price = item.price || 0;
      total += price * (item.quantity || 1);
    }
    return { items: parsed.items, total: parseFloat(total.toFixed(2)) };
  } catch (e) {
    return { items: [], total: 0 };
  }
}

function _saveLocalCart(cart) {
  localStorage.setItem('rawjoy_cart_hybrid', JSON.stringify(cart));
}

function _addToLocalCart(product, quantity, variant) {
  const cart = _getLocalCart();
  const price = product.price || 0;
  const existingIndex = cart.items.findIndex(item => item.productId === product.id && item.variant === variant);

  if (existingIndex >= 0) {
    cart.items[existingIndex].quantity += quantity;
  } else {
    cart.items.push({
      productId: product.id,
      name: product.name,
      price: price,
      quantity: quantity,
      image: product.mainImage || product.images?.[0] || product.image || '',
      variant: variant,
      slug: product.slug
    });
  }
  _saveLocalCart(cart);
  return { success: true, itemCount: cart.items.reduce((sum, i) => sum + i.quantity, 0) };
}

/**
 * Extract product info from the DOM context that triggered the add-to-cart.
 * Uses data attributes on quick-add-component and product-card elements.
 */
function extractProductFromDOM(shopifyVariantId) {
  // Strategy 1: Find the form → quick-add-component → read data attributes
  const hiddenInput = document.querySelector(`input[name="id"][value="${shopifyVariantId}"]`);
  if (!hiddenInput) {
    console.warn('[DB Bridge] Could not find input for variant:', shopifyVariantId);
    return null;
  }

  const form = hiddenInput.closest('form');
  if (!form) return null;

  // The quick-add-component has data-product-title and data-product-url!
  const quickAdd = form.closest('quick-add-component');
  const productCard = form.closest('product-card');
  const container = quickAdd || productCard || form.closest('.shopify-section');

  let name = '';
  let slug = '';
  let price = 0;
  let image = '';

  // Read from quick-add-component data attributes (most reliable)
  if (quickAdd) {
    name = quickAdd.getAttribute('data-product-title') || '';
    const productUrl = quickAdd.getAttribute('data-product-url') || '';
    const urlMatch = productUrl.match(/products\/([^/?#]+)/);
    if (urlMatch) slug = urlMatch[1];
  }

  // Read from product-card if available
  if (productCard) {
    // Title from product-card__title
    if (!name) {
      const titleEl = productCard.querySelector('.product-card__title .reversed-link__text');
      if (titleEl) name = titleEl.textContent.trim();
    }
    // Slug from product-card__link
    if (!slug) {
      const link = productCard.querySelector('a.product-card__link[href*="products/"]') ||
                   productCard.querySelector('a[href*="products/"]');
      if (link) {
        const href = link.getAttribute('href');
        const match = href.match(/products\/([^/?#]+)/);
        if (match) slug = match[1];
      }
    }
    // Price from product-price
    const priceEl = productCard.querySelector('product-price .price__regular .price') ||
                    productCard.querySelector('product-price .price');
    if (priceEl) {
      const priceText = priceEl.textContent.replace(/[^0-9.,]/g, '').replace(',', '.');
      price = parseFloat(priceText) || 0;
    }
    // Image - try src first, then data-srcset
    const imgEl = productCard.querySelector('img.product-card-main-image') ||
                  productCard.querySelector('.product-card__image img');
    if (imgEl) {
      image = imgEl.getAttribute('src') || '';
      if (!image || image === '') {
        // Try data-srcset (Shopify lazy loading pattern)
        const srcset = imgEl.getAttribute('data-srcset') || imgEl.getAttribute('srcset') || '';
        if (srcset) {
          // Get the first URL from srcset
          const firstUrl = srcset.split(',')[0].trim().split(/\s+/)[0];
          if (firstUrl) image = firstUrl;
        }
      }
    }
  }

  // Fallback: try reading from dialog/modal if this is a quick-add modal
  if (!name || !slug) {
    const dialog = form.closest('dialog') || document.querySelector('dialog[open]');
    if (dialog) {
      const qaComp = dialog.querySelector('quick-add-component');
      if (qaComp) {
        if (!name) name = qaComp.getAttribute('data-product-title') || '';
        const pUrl = qaComp.getAttribute('data-product-url') || '';
        if (!slug) {
          const m = pUrl.match(/products\/([^/?#]+)/);
          if (m) slug = m[1];
        }
      }
      // Price from dialog
      if (!price) {
        const dp = dialog.querySelector('.price__regular .price') || dialog.querySelector('.price');
        if (dp) {
          price = parseFloat(dp.textContent.replace(/[^0-9.,]/g, '').replace(',', '.')) || 0;
        }
      }
      // Image from dialog
      if (!image) {
        const di = dialog.querySelector('.product__media img') || dialog.querySelector('img.media__image');
        if (di) {
          image = di.getAttribute('src') || '';
          if (!image) {
            const ss = di.getAttribute('data-srcset') || di.getAttribute('srcset') || '';
            const fu = ss.split(',')[0].trim().split(/\s+/)[0];
            if (fu) image = fu;
          }
        }
      }
    }
  }

  // Extract variant from selected radio
  let variantName = null;
  const selectedRadio = (container || document).querySelector('input[type="radio"]:checked');
  if (selectedRadio) {
    variantName = selectedRadio.value || null;
  }

  if (!name && !slug) {
    console.warn('[DB Bridge] Could not extract product name or slug for variant:', shopifyVariantId);
    return null;
  }

  console.log('[DB Bridge] Extracted product from DOM:', { name, slug, price, image: image?.substring(0, 60) });

  return {
    id: slug || String(shopifyVariantId),
    name: name || slug,
    slug: slug,
    price: price,
    mainImage: image,
    variant: variantName,
    variants: variantName ? [{ name: variantName, price: price }] : []
  };
}

function getLocalProductImage(item, prefix) {
  if (!item) return '';
  var slug = item.slug;

  // Direct mapping to ensure correct product images
  var slugMapping = {
    "beef-spinach-stew": "beef-spinach-stew/images/BeefSpinachStew-361.jpg",
    "cat-calming-formula": "cat-calming-formula/images/CatCalmingFormula-345.jpg",
    "cat-wellness-mix": "cat-wellness-mix/images/CatWellnessMix-341.jpg",
    "chicken-bone-treat": "chicken-bone-treat/images/ChickenBoneTreat-418.jpg",
    "chicken-herb-stick": "chicken-herb-stick/images/ChickenHerbStick-409.jpg",
    "chicken-pumpkin-pate": "chicken-pumpkin-pate/images/ChickenPumpkinPate-357.jpg",
    "crunchy-bone-treat": "crunchy-bone-treat/images/CrunchyBoneTreat-373.jpg",
    "doggy-dental-mix": "doggy-dental-mix/images/DailyNutritionMix-1.jpg",
    "duck-soft-chews": "duck-soft-chews/images/DuckSoftChews-353.jpg",
    "fish-bone-treat": "fish-bone-treat/images/FishBoneTreat-413.jpg",
    "juicy-turkey-crunch": "juicy-turkey-crunch/images/JuicyTurkeyCrunch-349.jpg",
    "juicy-turkey-stick": "juicy-turkey-stick/images/JuicyTurkeyStick-401.jpg",
    "lamb-quinoa-blend": "lamb-quinoa-blend/images/LambQuinoaBlend-393.jpg",
    "mackerel-salmon-kibble": "mackerel-salmon-kibble/images/MackerelSalmonKibble-381.jpg",
    "mint-comfort-bowl-series": "mint-comfort-bowl-series/images/MintComfortBowlSeries-431.jpg",
    "pastel-pet-bowl-series": "pastel-pet-bowl-series/images/PastelPetBowlSeries-427.jpg",
    "pet-meal-time-mix": "pet-meal-time-mix/images/PetMealTimeMix-337.jpg",
    "rawjoy-blue-energy-bar": "rawjoy-blue-energy-bar/images/RawJoyBlueEnergyBar-423.jpg",
    "rawjoy-green-bar": "rawjoy-green-bar/images/RawJoyGreenBar-377.jpg",
    "rawjoy-soft-bar": "rawjoy-soft-bar/images/RawJoySoftBar-369.jpg",
    "salmon-broccoli-crunch": "salmon-broccoli-crunch/images/SalmonBroccoliCrunch-385.jpg",
    "salmon-carrot-pate": "salmon-carrot-pate/images/SalmonCarrotPate-365.jpg",
    "salmon-rice-formula": "salmon-rice-formula/images/SalmonRiceFormula-389.jpg",
    "salmon-stick": "salmon-stick/images/SalmonStick-405.jpg",
    "venison-peas-recipe": "venison-peas-recipe/images/VenisonPeasRecipe-397.jpg"
  };

  if (slug && slugMapping[slug]) {
    return prefix + folderSeparator + slugMapping[slug];
  }

  if (!slug) {
    var img = item.image || '';
    if (img && img.indexOf('http') !== 0 && img.indexOf('/') !== 0) {
      return prefix + img;
    }
    return img;
  }
  var img = item.image || '';
  if (img && (img.indexOf('products/') !== -1 || img.indexOf('products_') !== -1) && img.indexOf('images/') !== -1) {
    if (img.indexOf('http') !== 0 && img.indexOf('/') !== 0) {
      return prefix + img;
    }
    return img;
  }
  if (img) {
    var urlPart = img.split('?')[0];
    var parts = urlPart.split('/');
    var filename = parts[parts.length - 1];
    filename = decodeURIComponent(filename);
    if (filename && filename.indexOf('.') !== -1 && filename.toLowerCase().indexOf('product-img-') === -1) {
      return prefix + folderSeparator + slug + '/images/' + filename;
    }
  }
  return prefix + folderSeparator + slug + '/images/244b938eff304bb693951931814539b9.thumbnail.0000000000.jpg';
}

function renderCartDrawerHTML(cart, sectionId, depthPrefix) {
  if (cart && cart.items) {
    cart.items = cart.items.filter(item => !isDummyBundleProduct(item));
  }

  const totalItems = cart.items.reduce((sum, item) => sum + item.quantity, 0);
  const isEmpty = cart.items.length === 0;

  let originalTotal = 0;
  for (let i = 0; i < cart.items.length; i++) {
    const item = cart.items[i];
    originalTotal += item.price * item.quantity;
  }
  const totalStr = `$${originalTotal.toFixed(2)}`;
  const totalAmount = originalTotal;

  let isDialogOpen = false;
  try {
    const existingDialog = document.getElementById('cart-drawer-dialog');
    if (existingDialog && (existingDialog.open || existingDialog.hasAttribute('open'))) {
      isDialogOpen = true;
    }
  } catch(e) {}

  let rows = '';
  for (let i = 0; i < cart.items.length; i++) {
    const item = cart.items[i];
    const isSale = item.name.toLowerCase().indexOf('salmon stick') !== -1 || item.name.toLowerCase().indexOf('cat calming') !== -1;
    const comparePrice = isSale ? item.price * 1.4545 : null;
    
    const priceFormatted = '$' + (item.price || 0).toFixed(2);
    const compareFormatted = comparePrice ? '$' + comparePrice.toFixed(2) : null;

    let imgPath = getLocalProductImage(item, depthPrefix);

    const slug = item.slug || item.productId;
    const isBundleItem = bundleProducts.indexOf(slug) !== -1;
    const showItemDiscount = false;
    const discountedItemPrice = showItemDiscount ? item.price * 0.85 : item.price;
    const discountedPriceFormatted = '$' + discountedItemPrice.toFixed(2);

    rows += `
      <div class="cart-item-card" ref="cartItemRows[]" data-line="${i+1}">
        <div class="cart-item-image-wrapper">
          <a href="${depthPrefix}${folderSeparator}${item.slug}${fileSuffix}" tabindex="-1">
            <img src="${imgPath}" alt="${item.name}" loading="lazy">
          </a>
        </div>
        <div class="cart-item-details">
          <a class="cart-item-title reversed-link" href="${depthPrefix}${folderSeparator}${item.slug}${fileSuffix}"><span class="reversed-link__text">${item.name}</span></a>
          ${item.variant ? `<p class="cart-item-variant">${item.variant}</p>` : ''}
          ${showItemDiscount ? `<span class="bundle-badge">🎁 Bundle</span>` : ''}
          <div class="cart-item-actions">
            <div class="qty-pill">
              <button type="button" class="qty-btn" onclick="window.updateCartQty(${i+1}, ${item.quantity - 1})">-</button>
              <span class="qty-val">${item.quantity}</span>
              <button type="button" class="qty-btn" onclick="window.updateCartQty(${i+1}, ${item.quantity + 1})">+</button>
            </div>
            <a class="remove-link" onclick="window.updateCartQty(${i+1}, 0); return false;">Remove</a>
          </div>
        </div>
        <div class="cart-item-price-wrapper">
          ${showItemDiscount ? `<span class="sale-price">${discountedPriceFormatted}</span><span class="compare-price">${priceFormatted}</span>` : 
            `<span class="${isSale ? 'sale-price' : 'normal-price'}">${priceFormatted}</span>${compareFormatted ? `<span class="compare-price">${compareFormatted}</span>` : ''}`
          }
        </div>
      </div>
    `;
  }

  // Shipping goal calculation
  const threshold = 50;
  const remaining = threshold - totalAmount;
  let shippingText = '';
  const progressPercent = Math.min((totalAmount / threshold) * 100, 100);
  if (remaining > 0) {
    const remStr = '$' + remaining.toFixed(2);
    shippingText = `Spend <span style="font-weight: 700; color: #008a5b;">${remStr}</span> more to reach free shipping!`;
  } else {
    shippingText = "You've unlocked free shipping!";
  }

  // Filter recommended products
  const inCartSlugs = cart.items.map(item => item.slug || item.productId);
  const recommendedList = [
    {
      id: "chicken-bone-treat",
      name: "Chicken Bone",
      slug: "chicken-bone-treat",
      price: 22.00,
      image: "products/chicken-bone-treat/images/ChickenBoneTreat-418.jpg"
    },
    {
      id: "salmon-stick",
      name: "Salmon Stick",
      slug: "salmon-stick",
      price: 22.00,
      comparePrice: 32.00,
      image: "products/salmon-stick/images/SalmonStick-405.jpg"
    },
    {
      id: "cat-calming-formula",
      name: "Cat Calming",
      slug: "cat-calming-formula",
      price: 22.00,
      comparePrice: 32.00,
      image: "products/cat-calming-formula/images/CatCalmingFormula-345.jpg"
    }
  ];

  const filteredRecommended = recommendedList.filter(p => inCartSlugs.indexOf(p.slug) === -1);

  let recommendedCards = '';
  for (let j = 0; j < filteredRecommended.length; j++) {
    const rp = filteredRecommended[j];
    const rpPriceStr = '$' + rp.price.toFixed(2);
    const rpCompareStr = rp.comparePrice ? '$' + rp.comparePrice.toFixed(2) : null;
    const rpImg = rp.image ? (depthPrefix + rp.image.replace('products/', folderSeparator)) : '';
    
    recommendedCards += `
      <div class="complete-look-card">
        <div class="complete-look-img-wrapper">
          <img src="${rpImg}" alt="${rp.name}" loading="lazy">
        </div>
        <div class="complete-look-info">
          <span class="complete-look-name">${rp.name}</span>
          <div class="complete-look-price-row">
            <span class="complete-look-price ${rpCompareStr ? 'sale' : ''}">${rpPriceStr}</span>
            ${rpCompareStr ? `<span class="complete-look-compare">${rpCompareStr}</span>` : ''}
            ${rpCompareStr ? `<span class="complete-look-badge">Sale</span>` : ''}
          </div>
        </div>
        <button type="button" class="complete-look-add-btn" onclick="window.addRecommendedToCart('${rp.id}', this)">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>
        </button>
      </div>
    `;
  }

  let completeLookSection = '';
  if (filteredRecommended.length > 0) {
    completeLookSection = `
      <div class="complete-look-section">
        <div class="complete-look-header">
          <span class="complete-look-title">Complete The Look</span>
          <div class="complete-look-arrows">
            <button type="button" class="arrow-btn" onclick="var el = this.closest('.complete-look-section').querySelector('.complete-look-list'); el.scrollBy({left: -150, behavior: 'smooth'});">&lt;</button>
            <button type="button" class="arrow-btn" onclick="var el = this.closest('.complete-look-section').querySelector('.complete-look-list'); el.scrollBy({left: 150, behavior: 'smooth'});">&gt;</button>
          </div>
        </div>
        <div class="complete-look-list">
          ${recommendedCards}
        </div>
      </div>
    `;
  }

  return `
    <div class="shopify-section shopify-section-group-overlay-group" id="shopify-section-${sectionId}">
      <style>
        /* Custom styles injected directly to ensure 100% correct UI layout override */
        .shopify-section-group-overlay-group,
        [id^="shopify-section-"][id$="-drawer"] {
          position: relative !important;
          z-index: 999999 !important;
        }
        #cart-drawer-dialog {
          max-width: 480px !important;
          width: 100% !important;
          background: #ffffff !important;
          font-family: Poppins, sans-serif !important;
          z-index: 999999 !important;
        }
        .cart-drawer__inner {
          padding: 0 !important;
          display: flex;
          flex-direction: column;
          height: 100%;
        }
        .cart-items-component {
          display: flex;
          flex-direction: column;
          height: 100%;
        }
        .cart-drawer__header {
          padding: 20px !important;
          border-bottom: 1px solid #f0f0f0 !important;
          display: flex !important;
          align-items: center !important;
          justify-content: space-between !important;
        }
        .cart-drawer__heading {
          font-family: Poppins, sans-serif !important;
          font-weight: 700 !important;
          font-size: 2.2rem !important;
          color: #000000 !important;
          margin: 0 !important;
        }
        .cart-drawer__content {
          flex: 1 !important;
          overflow-y: auto !important;
          padding: 0 !important;
        }
        .cart-item-card {
          display: flex;
          align-items: center;
          padding: 16px 20px;
          border-bottom: 1px solid #f6f6f6;
          gap: 16px;
          background: #ffffff;
          transition: background-color 0.2s ease;
        }
        .cart-item-card:hover {
          background: #fafafa;
        }
        .cart-item-image-wrapper {
          width: 90px;
          height: 90px;
          border-radius: 12px;
          background: #f4f4f4;
          display: flex;
          align-items: center;
          justify-content: center;
          overflow: hidden;
          flex-shrink: 0;
        }
        .cart-item-image-wrapper img {
          max-width: 80%;
          max-height: 80%;
          object-fit: contain;
        }
        .cart-item-details {
          flex: 1;
          display: flex;
          flex-direction: column;
          gap: 4px;
          text-align: left;
        }
        .cart-item-title {
          font-size: 1.5rem;
          font-weight: 600;
          color: #000000;
          line-height: 1.3;
        }
        .cart-item-variant {
          font-size: 1.2rem;
          color: #888888;
        }
        .cart-item-actions {
          display: flex;
          align-items: center;
          margin-top: 8px;
          gap: 12px;
        }
        .qty-pill {
          border: 1px solid #e0e0e0;
          border-radius: 20px;
          display: inline-flex;
          align-items: center;
          padding: 3px 12px;
          gap: 12px;
          background: #ffffff;
        }
        .qty-btn {
          background: none;
          border: none;
          font-size: 1.6rem;
          font-weight: 700;
          cursor: pointer;
          color: #000000;
          padding: 0 4px;
          display: flex;
          align-items: center;
          justify-content: center;
          user-select: none;
        }
        .qty-btn:hover {
          color: #f05230;
        }
        .qty-val {
          font-weight: 600;
          font-size: 1.3rem;
          min-width: 16px;
          text-align: center;
        }
        .remove-link {
          color: #777777;
          font-size: 1.2rem;
          text-decoration: underline;
          cursor: pointer;
          font-weight: 500;
        }
        .remove-link:hover {
          color: #000000;
        }
        .cart-item-price-wrapper {
          display: flex;
          flex-direction: column;
          align-items: flex-end;
          justify-content: center;
          min-width: 70px;
        }
        .sale-price {
          font-size: 1.5rem;
          font-weight: 700;
          color: #f05230;
        }
        .normal-price {
          font-size: 1.5rem;
          font-weight: 700;
          color: #000000;
        }
        .compare-price {
          font-size: 1.3rem;
          text-decoration: line-through;
          color: #999999;
          margin-top: 2px;
        }
        .complete-look-section {
          background: #fafafa;
          border-top: 1px solid #eeeeee;
          padding: 20px 0 10px 0;
        }
        .complete-look-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0 20px 12px 20px;
        }
        .complete-look-title {
          font-size: 1.6rem;
          font-weight: 700;
          color: #000000;
          margin: 0;
        }
        .complete-look-arrows {
          display: flex;
          gap: 8px;
        }
        .arrow-btn {
          background: none;
          border: none;
          cursor: pointer;
          font-size: 1.6rem;
          font-weight: 700;
          color: #000000;
          padding: 4px;
          opacity: 0.6;
          transition: opacity 0.2s;
        }
        .arrow-btn:hover {
          opacity: 1;
        }
        .complete-look-list {
          display: flex;
          gap: 12px;
          padding: 0 20px 10px 20px;
          overflow-x: auto;
          scrollbar-width: none;
        }
        .complete-look-list::-webkit-scrollbar {
          display: none;
        }
        .complete-look-card {
          background: #ffffff;
          border: 1px solid #eeeeee;
          border-radius: 12px;
          padding: 12px;
          display: flex;
          align-items: center;
          gap: 12px;
          min-width: 250px;
          flex-shrink: 0;
          box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        }
        .complete-look-img-wrapper {
          width: 60px;
          height: 60px;
          border-radius: 8px;
          background: #f5f5f5;
          display: flex;
          align-items: center;
          justify-content: center;
          overflow: hidden;
          flex-shrink: 0;
        }
        .complete-look-img-wrapper img {
          max-width: 85%;
          max-height: 85%;
          object-fit: contain;
        }
        .complete-look-info {
          flex: 1;
          text-align: left;
          display: flex;
          flex-direction: column;
        }
        .complete-look-name {
          font-size: 1.35rem;
          font-weight: 600;
          color: #000000;
          line-height: 1.3;
        }
        .complete-look-price-row {
          display: flex;
          align-items: center;
          gap: 6px;
          margin-top: 4px;
        }
        .complete-look-price {
          font-size: 1.3rem;
          font-weight: 700;
          color: #000000;
        }
        .complete-look-price.sale {
          color: #f05230;
        }
        .complete-look-compare {
          font-size: 1.15rem;
          text-decoration: line-through;
          color: #999999;
        }
        .complete-look-badge {
          background: #ffebe7;
          color: #f05230;
          font-size: 1rem;
          font-weight: 700;
          padding: 1px 6px;
          border-radius: 4px;
          margin-left: 6px;
        }
        .complete-look-add-btn {
          width: 36px;
          height: 36px;
          border-radius: 50%;
          background: #000000;
          color: #ffffff;
          display: flex;
          align-items: center;
          justify-content: center;
          border: none;
          cursor: pointer;
          transition: transform 0.2s, background-color 0.2s;
          flex-shrink: 0;
        }
        .complete-look-add-btn:hover {
          background: #f05230;
          transform: scale(1.05);
        }
        .premium-cart-footer {
          background: #000000 !important;
          padding: 24px 20px !important;
          color: #ffffff !important;
          border-top: none !important;
          font-family: Poppins, sans-serif !important;
        }
        .footer-price-section {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 12px;
        }
        .footer-total-label {
          font-size: 1.3rem;
          color: #b0b0b0;
          text-transform: capitalize;
          font-weight: 500;
        }
        .footer-total-price {
          font-size: 3.2rem;
          font-weight: 700;
          color: #ffffff;
          margin-top: 4px;
        }
        .footer-actions {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-top: 4px;
        }
        .footer-icon-btn {
          width: 36px;
          height: 36px;
          border-radius: 50%;
          background: #222222;
          color: #ffffff;
          display: flex;
          align-items: center;
          justify-content: center;
          border: none;
          cursor: pointer;
          transition: background-color 0.2s;
        }
        .footer-icon-btn:hover {
          background: #333333;
        }
        .footer-disclaimer {
          font-size: 1.15rem;
          color: #888888;
          line-height: 1.4;
          margin-bottom: 18px;
          text-align: right;
        }
        .footer-buttons-row {
          display: flex;
          gap: 12px;
        }
        .footer-btn {
          flex: 1;
          border-radius: 30px;
          padding: 12px 0;
          font-size: 1.4rem;
          font-weight: 600;
          text-align: center;
          text-decoration: none !important;
          cursor: pointer;
          transition: all 0.2s ease;
          display: inline-block;
          box-sizing: border-box;
        }
        .footer-btn-outline {
          background: transparent;
          color: #ffffff;
          border: 1.5px solid #ffffff;
        }
        .footer-btn-outline:hover {
          background: #222222;
        }
        .footer-btn-filled {
          background: #ffffff;
          color: #000000;
          border: 1.5px solid #ffffff;
        }
        .footer-btn-filled:hover {
          background: #f0f0f0;
        }
      </style>
      <link href="${depthPrefix}css/cart-drawer.css" media="all" rel="stylesheet">
      <link href="${depthPrefix}css/cart-modules.css" media="all" rel="stylesheet">
      <script src="${depthPrefix}js/cart-drawer.js" type="module"></script>
      <script src="${depthPrefix}js/cart-items.js" type="module"></script>
      <script src="${depthPrefix}js/cart-shipping.js" type="module"></script>
      <script src="${depthPrefix}js/product-recommendations.js" type="module"></script>
      <cart-drawer-component auto-open="" class="cart-drawer" id="CartDrawer">
        <dialog ${isDialogOpen ? 'open=""' : ''} class="dialog dialog--drawer dialog--cart-drawer dialog--drawer-right overflow-hidden" id="cart-drawer-dialog" ref="dialog" scroll-lock="">
          <div class="cart-drawer__inner">
            <cart-items-component class="cart-items-component" data-section-id="${sectionId}">
              <span class="visually-hidden" ref="cartItemCount" style="display:none;">${totalItems}</span>
              <span class="cart-bubble__text-count" style="display:none;">${totalItems}</span>
              <div class="cart-drawer__header relative flex items-center justify-between gap-2" id="cart-drawer-header">
                <span class="cart-drawer__heading cart__heading relative h3" style="display:inline-flex; align-items:baseline;">Your cart
                  <sup style="font-size: 0.6em; font-weight: 700; margin-left: 2px; vertical-align: super; top: -0.5em; position: relative;">${totalItems}</sup>
                </span>
                <button class="cart-drawer__close dialog__close shrink-0" on:click="cart-drawer-component/close">
                  <span class="icon icon--close icon--large"><svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M0 0H20V20H0V0z" fill="none" height="256" width="256"></path><path d="M15.625 4.375L4.375 15.625" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="var(--icon-stroke-width, 2)"></path><path d="M15.625 15.625L4.375 4.375" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="var(--icon-stroke-width, 2)"></path></svg></span>
                </button>
              </div>
              <div class="cart-drawer__shipping-goal" style="padding: 15px 20px; font-family: Poppins, sans-serif; font-size: 1.4rem;">
                <div style="color: #008a5b; margin-bottom: 8px; font-weight: 500;">${shippingText}</div>
                <div style="background: #e8e8e8; border-radius: 10px; height: 6px; overflow: hidden; width: 100%;">
                  <div style="background: #008a5b; width: ${progressPercent}%; height: 100%; transition: width 0.3s ease; border-radius: 10px;"></div>
                </div>
              </div>
              <div class="cart-drawer__content">
                ${isEmpty ? `<div class="cart-drawer__empty text-center"><p>Your cart is empty</p></div>` : rows}
                ${!isEmpty ? completeLookSection : ''}
              </div>
              ${!isEmpty ? `
              <div class="premium-cart-footer">
                <div class="footer-price-section">
                  <div>
                    <div class="footer-total-label">Estimated total</div>
                    <div class="footer-total-price">${totalStr}</div>
                  </div>
                  <div class="footer-actions">
                    <button type="button" class="footer-icon-btn">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 1 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                    </button>
                    <button type="button" class="footer-icon-btn">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="16.5" y1="9.4" x2="7.5" y2="4.21"></line><polygon points="12 22.08 12 12 3 6.92 3 17.08 12 22.08"></polygon><polygon points="12 12 21 6.92 21 17.08 12 22.08"></polygon><polygon points="12 2 3 6.92 12 12 21 6.92 12 2"></polygon><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
                    </button>
                  </div>
                </div>
                <div class="footer-disclaimer">Taxes, discounts and shipping calculated at checkout.</div>
                <div class="footer-buttons-row">
                  <a class="footer-btn footer-btn-outline" href="${depthPrefix}cart/index.html">View Cart</a>
                  <a class="footer-btn footer-btn-filled" href="${depthPrefix}pages/checkout/index.html">Check Out</a>
                </div>
              </div>` : ''}
            </cart-items-component>
          </div>
        </dialog>
      </cart-drawer-component>
    </div>
  `;
}

// Global helper functions exposed for the custom cart buttons
if (typeof window.updateCartQty !== 'function') {
  window.updateCartQty = function(line, newQty) {
    console.log('[DB Bridge] updateCartQty line:', line, 'qty:', newQty);
    var event = new CustomEvent("quantity-selector:update", {
      bubbles: true,
      detail: { quantity: newQty, cartLine: line }
    });
    document.dispatchEvent(event);
  };
}

window.addRecommendedToCart = function(productId, btn) {
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = '<span style="font-size: 1.2rem;">...</span>';
  }
  
  // Determine the product page URL dynamically
  function getDepthPrefix() {
    var loc = window.location.pathname;
    var parts = loc.split('/').filter(Boolean);
    
    var rootIndicators = ['products', 'collections', 'pages', 'blogs', 'policies', 'cart', 'search', 'contact', 'css', 'js', 'images', 'firebase', 'data', 'api'];
    var rootIndex = -1;
    for (var i = 0; i < parts.length; i++) {
      if (rootIndicators.indexOf(parts[i].toLowerCase()) !== -1) {
        rootIndex = i;
        break;
      }
    }
    
    var depth = 0;
    if (rootIndex !== -1) {
      var remaining = parts.slice(rootIndex);
      if (remaining.length > 0) {
        var last = remaining[remaining.length - 1];
        if (last.indexOf('.') !== -1) {
          remaining.pop();
        }
      }
      depth = remaining.length;
    } else {
      var index = -1;
      for (var i = 0; i < parts.length; i++) {
        var pLower = parts[i].toLowerCase();
        if (pLower === 'rawjoy' || pLower === 'op' || pLower === 'homepage') {
          index = i;
          break;
        }
      }
      var relevantParts = index !== -1 ? parts.slice(index + 1) : parts;
      if (relevantParts.length > 0) {
        var last = relevantParts[relevantParts.length - 1];
        if (last.indexOf('.') !== -1) {
          relevantParts.pop();
        }
      }
      depth = relevantParts.length;
    }
    
    if (depth <= 0) return './';
    return new Array(depth + 1).join('../');
  }

  var prefix = getDepthPrefix();
  var productPageUrl = prefix + folderSeparator + productId + (isFlattened ? '/index.html' : '/');
  
  // Fetch the recommended product page HTML
  originalFetch(productPageUrl)
    .then(function(res) {
      if (!res.ok) throw new Error('Failed to fetch product page');
      return res.text();
    })
    .then(function(responseText) {
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>';
      }
      
      var parser = new DOMParser();
      var htmlDoc = parser.parseFromString(responseText, 'text/html');
      var quickAddContent = htmlDoc.querySelector('[data-quick-add-content]');
      
      if (!quickAddContent) {
        throw new Error('Could not find data-quick-add-content on target page');
      }
      
      // Resolve relative paths inside the loaded HTML relative to the current page location
      var baseUrl = productPageUrl.split('?')[0];
      if (!baseUrl.endsWith('/') && !baseUrl.match(/\.[a-zA-Z0-9]+$/)) {
        baseUrl += '/';
      }
      
      function getSubfolderPrefix() {
        var pathname = window.location.pathname;
        var parts = pathname.split('/').filter(Boolean);
        var rootIndicators = ['products', 'collections', 'pages', 'blogs', 'policies', 'cart', 'search', 'contact', 'css', 'js', 'images', 'firebase', 'data', 'api'];
        var knownPages = ['index.html', 'index.php'];
        var subfolder = '';
        for (var i = 0; i < parts.length; i++) {
          var pLower = parts[i].toLowerCase();
          if (rootIndicators.indexOf(pLower) !== -1 || knownPages.indexOf(pLower) !== -1 || pLower.indexOf('.') !== -1) {
            if (i > 0) {
              subfolder = '/' + parts.slice(0, i).join('/') + '/';
            }
            break;
          }
        }
        if (subfolder) return subfolder;
        return '/';
      }

      function resolveUrl(relUrl) {
        if (!relUrl || relUrl.startsWith('http:') || relUrl.startsWith('https:') || relUrl.startsWith('data:')) {
          return relUrl;
        }
        if (relUrl.startsWith('/')) {
          var subfolderPrefix = getSubfolderPrefix();
          var res = relUrl;
          if (subfolderPrefix !== '/') {
            if (!relUrl.toLowerCase().startsWith(subfolderPrefix.toLowerCase())) {
              res = subfolderPrefix + relUrl.substring(1);
            }
          }
          return res;
        }
        try {
          return new URL(relUrl, new URL(baseUrl, window.location.href)).toString();
        } catch(e) {
          return relUrl;
        }
      }
      
      quickAddContent.querySelectorAll('img, source, video').forEach(function(el) {
        if (el.hasAttribute('src')) {
          el.setAttribute('src', resolveUrl(el.getAttribute('src')));
        }
        if (el.hasAttribute('srcset')) {
          var srcset = el.getAttribute('srcset');
          if (srcset) {
            var parts = srcset.split(',').map(function(part) {
              var trimmed = part.trim();
              if (!trimmed) return '';
              var match = trimmed.match(/^(\S+)(.*)$/);
              if (match) {
                return resolveUrl(match[1]) + match[2];
              }
              return trimmed;
            });
            el.setAttribute('srcset', parts.filter(Boolean).join(', '));
          }
        }
      });
      
      quickAddContent.querySelectorAll('a').forEach(function(el) {
        if (el.hasAttribute('href')) {
          el.setAttribute('href', resolveUrl(el.getAttribute('href')));
        }
      });
      
      quickAddContent.querySelectorAll('form').forEach(function(el) {
        if (el.hasAttribute('action')) {
          el.setAttribute('action', resolveUrl(el.getAttribute('action')));
        }
      });

      // Resolve data-product-url on quickAddContent itself and any descendants
      if (quickAddContent.hasAttribute('data-product-url')) {
        quickAddContent.setAttribute('data-product-url', resolveUrl(quickAddContent.getAttribute('data-product-url')));
      }
      quickAddContent.querySelectorAll('[data-product-url]').forEach(function(el) {
        el.setAttribute('data-product-url', resolveUrl(el.getAttribute('data-product-url')));
      });

      // Update the quick add modal content and open it
      var quickAddDrawerContent = document.getElementById('quick-add-drawer-content');
      var dialogComponent = document.getElementById('quick-add-dialog');
      
      if (quickAddDrawerContent && dialogComponent) {
        quickAddDrawerContent.innerHTML = quickAddContent.innerHTML;
        
        // Close the cart drawer dialog first to prevent overlapping screens
        /*
        var cartDrawerDialog = document.getElementById('cart-drawer-dialog');
        if (cartDrawerDialog && typeof cartDrawerDialog.close === 'function') {
          cartDrawerDialog.close();
          cartDrawerDialog.removeAttribute('open');
        }
        */
        
        // Show the quick add modal
        if (typeof dialogComponent.showDialog === 'function') {
          dialogComponent.showDialog();
        } else {
          dialogComponent.setAttribute('open', '');
        }
      }
    })
    .catch(function(err) {
      console.error('[Complete the Look] Failed to open options popup:', err);
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = '!';
      }
      // Fallback: Redirect to the product page directly
      window.location.href = productPageUrl;
    });
};

// Fetch interceptor has been moved to cart-interceptor.js to ensure it runs synchronously in the head

// ============================================================
// 2. FIREBASE DISABLED (Laragon Local PHP & MySQL Mode)
// ============================================================

// ============================================================
// 3. HELPERS
// ============================================================

function isOnline() {
  return navigator.onLine;
}

function hasAndroidBridge() {
  return typeof window.AndroidDB !== 'undefined';
}

// Full LocalStorage DB (reuses the same _getLocalCart/_saveLocalCart above)
const LocalStorageDB = {
  getCart: _getLocalCart,
  saveCart: _saveLocalCart,
  addToCart: _addToLocalCart,
  updateCartItem(productId, quantity, variant) {
    const cart = _getLocalCart();
    const index = cart.items.findIndex(item => item.productId === productId && item.variant === variant);
    if (index >= 0) {
      if (quantity <= 0) {
        cart.items.splice(index, 1);
      } else {
        cart.items[index].quantity = quantity;
      }
      _saveLocalCart(cart);
      return { success: true };
    }
    return { success: false };
  },
  clearCart() {
    _saveLocalCart({ items: [] });
    return { success: true };
  },
  getOrders() {
    const data = localStorage.getItem('rawjoy_orders_hybrid') || '[]';
    return JSON.parse(data);
  },
  createOrder(orderData) {
    const orders = this.getOrders();
    const newOrder = {
      id: 'local_' + Date.now(),
      ...orderData,
      status: 'pending',
      createdAt: new Date().toISOString()
    };
    orders.push(newOrder);
    localStorage.setItem('rawjoy_orders_hybrid', JSON.stringify(orders));
    this.clearCart();
    return { success: true, orderId: newOrder.id };
  }
};

// ============================================================
// 4. UNIFIED DB API (PHP + MySQL API wrapper & offline LocalStorage fallback)
// ============================================================

const isWebServer = window.location.protocol.startsWith('http');

function getGlobalDepthPrefix() {
  const pathParts = window.location.pathname.split('/').filter(Boolean);
  const rootIndicators = ['products', 'collections', 'pages', 'blogs', 'policies', 'cart', 'search', 'contact', 'css', 'js', 'images', 'firebase', 'data', 'api'];
  let rootIndex = -1;
  for (let i = 0; i < pathParts.length; i++) {
    if (rootIndicators.includes(pathParts[i].toLowerCase())) {
      rootIndex = i;
      break;
    }
  }
  let depth = 0;
  if (rootIndex !== -1) {
    let remaining = pathParts.slice(rootIndex);
    if (remaining.length > 0) {
      let last = remaining[remaining.length - 1];
      if (last.includes('.')) {
        remaining.pop();
      }
    }
    depth = remaining.length;
  } else {
    let index = pathParts.findIndex(p => p.toLowerCase() === 'rawjoy' || p.toLowerCase() === 'op');
    if (index !== -1) {
      let remaining = pathParts.slice(index + 1);
      if (remaining.length > 0) {
        let last = remaining[remaining.length - 1];
        if (last.includes('.')) {
          remaining.pop();
        }
      }
      depth = remaining.length;
    } else {
      let remaining = [...pathParts];
      if (remaining.length > 0) {
        let last = remaining[remaining.length - 1];
        if (last.includes('.')) {
          remaining.pop();
        }
      }
      if (remaining.length > 0) {
        remaining.shift();
      }
      depth = remaining.length;
    }
  }
  return depth > 0 ? '../'.repeat(depth) : './';
}
const globalPrefix = getGlobalDepthPrefix();

function getApiUrl(endpoint) {
  return globalPrefix + 'api/' + endpoint;
}

async function apiFetch(endpoint, options = {}) {
  const url = getApiUrl(endpoint);
  options.credentials = 'same-origin';
  
  if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
    options.body = JSON.stringify(options.body);
    options.headers = {
      ...options.headers,
      'Content-Type': 'application/json'
    };
  }
  
  const response = await fetch(url, options);
  if (!response.ok) {
    const errData = await response.json().catch(() => ({}));
    throw new Error(errData.error || `HTTP error! status: ${response.status}`);
  }
  return await response.json();
}

const authListeners = [];

function notifyAuthChange(user) {
  for (const listener of authListeners) {
    try {
      listener(user);
    } catch (e) {
      console.error('[DB Bridge] Auth listener error:', e);
    }
  }
}

export const DB = {
  auth: {
    async register(email, password, name, phone = '') {
      if (isWebServer) {
        try {
          const res = await apiFetch('auth.php?action=register', {
            method: 'POST',
            body: { email, password, name, phone }
          });
          if (res.success && res.user) {
            localStorage.setItem('rawjoy_logged_in_user', JSON.stringify(res.user));
            notifyAuthChange(res.user);
          }
          return res;
        } catch (e) {
          return { success: false, error: e.message };
        }
      }
      return { success: false, error: 'Registrasi membutuhkan server web lokal.' };
    },
    async login(email, password) {
      if (isWebServer) {
        try {
          const res = await apiFetch('auth.php?action=login', {
            method: 'POST',
            body: { email, password }
          });
          if (res.success && res.user) {
            localStorage.setItem('rawjoy_logged_in_user', JSON.stringify(res.user));
            notifyAuthChange(res.user);
          }
          return res;
        } catch (e) {
          return { success: false, error: e.message };
        }
      }
      if (email === 'offline@rawjoy.com') {
        const dummyUser = { uid: 'offline_user', email, displayName: 'Offline User' };
        localStorage.setItem('offline_user', JSON.stringify(dummyUser));
        return { success: true, user: dummyUser };
      }
      return { success: false, error: 'Login membutuhkan server web lokal.' };
    },
    async logout() {
      if (isWebServer) {
        try {
          const res = await apiFetch('auth.php?action=logout', { method: 'POST' });
          localStorage.removeItem('rawjoy_logged_in_user');
          notifyAuthChange(null);
          return res;
        } catch (e) {
          return { success: false, error: e.message };
        }
      }
      localStorage.removeItem('offline_user');
      return { success: true };
    },
    getCurrentUser() {
      if (isWebServer) {
        const local = localStorage.getItem('rawjoy_logged_in_user');
        return local ? JSON.parse(local) : null;
      }
      const local = localStorage.getItem('offline_user');
      return local ? JSON.parse(local) : null;
    },
    onAuthChange(callback) {
      if (isWebServer) {
        authListeners.push(callback);
        const currentUser = this.getCurrentUser();
        setTimeout(() => callback(currentUser), 0);
        return () => {
          const index = authListeners.indexOf(callback);
          if (index !== -1) authListeners.splice(index, 1);
        };
      }
      const user = this.getCurrentUser();
      setTimeout(() => callback(user), 0);
      return () => {};
    },
    async getProfile(uid) {
      if (isWebServer) {
        try {
          return await apiFetch('auth.php?action=get_profile' + (uid ? '&uid=' + uid : ''));
        } catch (e) {
          return { success: false, error: e.message };
        }
      }
      return { success: true, data: { name: 'Offline User', email: 'offline@rawjoy.com', phone: '', address: 'Mode Offline' } };
    },
    async updateProfile(uid, data) {
      if (isWebServer) {
        try {
          const res = await apiFetch('auth.php?action=update_profile' + (uid ? '&uid=' + uid : ''), {
            method: 'POST',
            body: data
          });
          if (res.success) {
            const currentUser = this.getCurrentUser();
            if (currentUser && currentUser.uid == uid) {
              currentUser.displayName = data.name;
              localStorage.setItem('rawjoy_logged_in_user', JSON.stringify(currentUser));
              notifyAuthChange(currentUser);
            }
          }
          return res;
        } catch (e) {
          return { success: false, error: e.message };
        }
      }
      return { success: false, error: 'Update profile membutuhkan server web lokal.' };
    }
  },

  products: {
    async getAll(options = {}) {
      if (isWebServer) {
        try {
          let url = 'products.php?action=all';
          if (options.category) {
            url += '&category=' + encodeURIComponent(options.category);
          }
          return await apiFetch(url);
        } catch (e) {
          console.error('[DB Bridge] PHP products fetch failed:', e);
        }
      }
      if (hasAndroidBridge()) {
        try { return JSON.parse(window.AndroidDB.getProducts(JSON.stringify(options))); } catch(e) { console.error(e); }
      }
      const response = await fetch(globalPrefix + 'js/seed-data.json');
      const data = await response.json();
      let list = data.products || [];
      if (options.category) list = list.filter(p => p.category.toLowerCase() === options.category.toLowerCase());
      return list;
    },
    async getBySlug(slug) {
      if (isWebServer) {
        try {
          return await apiFetch('products.php?action=by_slug&slug=' + encodeURIComponent(slug));
        } catch (e) {
          console.error('[DB Bridge] PHP product by slug failed:', e);
        }
      }
      if (hasAndroidBridge()) {
        try { const r = window.AndroidDB.getProductBySlug(slug); return r ? JSON.parse(r) : null; } catch(e) { console.error(e); }
      }
      const all = await this.getAll();
      return all.find(p => p.slug === slug) || null;
    },
    async getById(id) {
      if (isWebServer) {
        try {
          return await apiFetch('products.php?action=by_id&id=' + encodeURIComponent(id));
        } catch (e) {
          console.error('[DB Bridge] PHP product by ID failed:', e);
        }
      }
      const all = await this.getAll();
      return all.find(p => p.id === id) || null;
    },
    async search(term) {
      if (isWebServer) {
        try {
          return await apiFetch('products.php?action=search&term=' + encodeURIComponent(term));
        } catch (e) {
          console.error('[DB Bridge] PHP products search failed:', e);
        }
      }
      const all = await this.getAll();
      const t = term.toLowerCase();
      return all.filter(p => p.name.toLowerCase().includes(t) || p.description?.toLowerCase().includes(t));
    }
  },

  cart: {
    async get() {
      if (isWebServer) {
        try {
          const cart = await apiFetch('cart.php?action=get');
          _saveLocalCart(cart);
          return cart;
        } catch (e) {
          console.error('[DB Bridge] PHP cart get failed, using LocalStorage:', e);
        }
      }
      let cart;
      if (hasAndroidBridge()) {
        try {
          const items = JSON.parse(window.AndroidDB.getCartItems());
          cart = { items, total: items.reduce((s, i) => s + (i.price * i.quantity), 0) };
        } catch(e) {
          console.error(e);
          cart = _getLocalCart();
        }
      } else {
        cart = _getLocalCart();
      }

      // Self-heal stale cart items (fix missing images, names, prices)
      if (cart && cart.items) {
        let needsSave = false;
        for (const item of cart.items) {
          if (!item.image || item.image.includes('244b938eff304bb693951931814539b9') || item.price === 0) {
            try {
              const slug = item.slug || item.productId;
              const slugMapping = {
                'beef-spinach-stew': 'products/beef-spinach-stew/images/BeefSpinachStew-361.jpg',
                'cat-calming-formula': 'products/cat-calming-formula/images/CatCalmingFormula-345.jpg',
                'cat-wellness-mix': 'products/cat-wellness-mix/images/CatWellnessMix-341.jpg',
                'chicken-bone-treat': 'products/chicken-bone-treat/images/ChickenBoneTreat-418.jpg',
                'chicken-herb-stick': 'products/chicken-herb-stick/images/ChickenHerbStick-409.jpg',
                'chicken-pumpkin-pate': 'products/chicken-pumpkin-pate/images/ChickenPumpkinPate-357.jpg',
                'crunchy-bone-treat': 'products/crunchy-bone-treat/images/CrunchyBoneTreat-373.jpg',
                'doggy-dental-mix': 'products/doggy-dental-mix/images/DailyNutritionMix-1.jpg',
                'duck-soft-chews': 'products/duck-soft-chews/images/DuckSoftChews-353.jpg',
                'fish-bone-treat': 'products/fish-bone-treat/images/FishBoneTreat-413.jpg',
                'juicy-turkey-crunch': 'products/juicy-turkey-crunch/images/JuicyTurkeyCrunch-349.jpg',
                'juicy-turkey-stick': 'products/juicy-turkey-stick/images/JuicyTurkeyStick-401.jpg',
                'lamb-quinoa-blend': 'products/lamb-quinoa-blend/images/LambQuinoaBlend-393.jpg',
                'mackerel-salmon-kibble': 'products/mackerel-salmon-kibble/images/MackerelSalmonKibble-381.jpg',
                'mint-comfort-bowl-series': 'products/mint-comfort-bowl-series/images/MintComfortBowlSeries-431.jpg',
                'pastel-pet-bowl-series': 'products/pastel-pet-bowl-series/images/PastelPetBowlSeries-427.jpg',
                'pet-meal-time-mix': 'products/pet-meal-time-mix/images/PetMealTimeMix-337.jpg',
                'rawjoy-blue-energy-bar': 'products/rawjoy-blue-energy-bar/images/RawJoyBlueEnergyBar-423.jpg',
                'rawjoy-green-bar': 'products/rawjoy-green-bar/images/RawJoyGreenBar-377.jpg',
                'rawjoy-soft-bar': 'products/rawjoy-soft-bar/images/RawJoySoftBar-369.jpg',
                'salmon-broccoli-crunch': 'products/salmon-broccoli-crunch/images/SalmonBroccoliCrunch-385.jpg',
                'salmon-carrot-pate': 'products/salmon-carrot-pate/images/SalmonCarrotPate-365.jpg',
                'salmon-rice-formula': 'products/salmon-rice-formula/images/SalmonRiceFormula-389.jpg',
                'salmon-stick': 'products/salmon-stick/images/SalmonStick-405.jpg',
                'venison-peas-recipe': 'products/venison-peas-recipe/images/VenisonPeasRecipe-397.jpg'
              };
              if (slug && slugMapping[slug]) {
                item.image = slugMapping[slug];
                needsSave = true;
              }
            } catch (e) {
              console.error('[DB Bridge] Failed to heal cart item:', item.productId, e);
            }
          }
        }
        const bundleProducts = [
          'cat-wellness-mix',
          'duck-soft-chews',
          'lamb-quinoa-blend',
          'salmon-rice-formula',
          'juicy-turkey-crunch',
          'pet-meal-time-mix'
        ];
        
        let total = 0;
        for (let i = 0; i < cart.items.length; i++) {
          const item = cart.items[i];
          let price = item.price || 0;
          total += price * (item.quantity || 1);
        }
        cart.total = Math.round(total);
        if (needsSave) _saveLocalCart(cart);
      }
      return cart;
    },
    async add(product, quantity = 1, variant = null) {
      if (isWebServer) {
        try {
          const res = await apiFetch('cart.php?action=add', {
            method: 'POST',
            body: { productId: product.id, quantity, variant }
          });
          const updatedCart = await apiFetch('cart.php?action=get');
          _saveLocalCart(updatedCart);
          return res;
        } catch (e) {
          console.error('[DB Bridge] PHP cart add failed, using LocalStorage:', e);
        }
      }
      if (hasAndroidBridge()) {
        try { return JSON.parse(window.AndroidDB.addToCart(product.id, product.name, variant || '', product.price, product.mainImage || '', quantity)); } catch(e) { console.error(e); }
      }
      return _addToLocalCart(product, quantity, variant);
    },
    async update(productId, quantity, variant = null) {
      if (isWebServer) {
        try {
          const res = await apiFetch('cart.php?action=update', {
            method: 'POST',
            body: { productId, quantity, variant }
          });
          const updatedCart = await apiFetch('cart.php?action=get');
          _saveLocalCart(updatedCart);
          return res;
        } catch (e) {
          console.error('[DB Bridge] PHP cart update failed, using LocalStorage:', e);
        }
      }
      if (hasAndroidBridge()) {
        try { return JSON.parse(window.AndroidDB.updateCartItem(productId, variant || '', quantity)); } catch(e) { console.error(e); }
      }
      return LocalStorageDB.updateCartItem(productId, quantity, variant);
    },
    async remove(productId, variant = null) { return this.update(productId, 0, variant); },
    async clear() {
      if (isWebServer) {
        try {
          const res = await apiFetch('cart.php?action=clear', { method: 'POST' });
          _saveLocalCart({ items: [], total: 0 });
          return res;
        } catch (e) {
          console.error('[DB Bridge] PHP cart clear failed, using LocalStorage:', e);
        }
      }
      if (hasAndroidBridge()) { try { window.AndroidDB.clearCart(); return { success: true }; } catch(e) { console.error(e); } }
      return LocalStorageDB.clearCart();
    },
    async getCount() {
      const cart = await this.get();
      return cart.items.reduce((sum, item) => sum + item.quantity, 0);
    }
  },

  orders: {
    async create(orderData) {
      if (isWebServer) {
        try {
          return await apiFetch('orders.php?action=create', {
            method: 'POST',
            body: orderData
          });
        } catch (e) {
          return { success: false, error: e.message };
        }
      }
      if (hasAndroidBridge()) {
        try { return JSON.parse(window.AndroidDB.createOrder(JSON.stringify({ ...orderData, synced: 0 }))); } catch(e) { console.error(e); }
      }
      return LocalStorageDB.createOrder(orderData);
    },
    async getUserOrders() {
      if (isWebServer) {
        try {
          return await apiFetch('orders.php?action=user_orders');
        } catch (e) {
          console.error('[DB Bridge] PHP orders fetch failed:', e);
        }
      }
      if (hasAndroidBridge()) { try { return JSON.parse(window.AndroidDB.getUserOrders()); } catch(e) { console.error(e); } }
      return LocalStorageDB.getOrders();
    }
  },

  async syncOfflineData() {
    // Firebase sync removed, local-only bridge
  }
};

// Expose DB globally so non-module scripts like cart-interceptor can use it
window.DB = DB;

// Auto-sync when online
if (hasAndroidBridge()) {
  window.addEventListener('online', () => DB.syncOfflineData());
  setTimeout(() => DB.syncOfflineData(), 3000);
}

// Update cart count badges from unified DB after initialization
DB.cart.get().then(cart => {
  const totalItems = cart.items.reduce((sum, item) => sum + item.quantity, 0);
  if (typeof window.updateCartBadges === 'function') {
    window.updateCartBadges(totalItems);
  }
  if (typeof window.updateAndInjectCart === 'function') {
    window.updateAndInjectCart();
  }
}).catch(console.error);
