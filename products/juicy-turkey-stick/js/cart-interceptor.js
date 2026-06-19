/**
 * Cart Fetch Interceptor — RawJoy Hybrid App
 * MUST be loaded as a regular <script> (NOT type="module") before any other scripts.
 * Intercepts all /cart/add, /cart/change, /cart/update, /cart/clear, /cart.js requests
 * and routes them to LocalStorage-based cart management.
 */
(function() {
  'use strict';

  if (window.__rawjoyInterceptorInstalled) return;
  window.__rawjoyInterceptorInstalled = true;

  // Disable Shopify dynamic storefront feature autoloading to prevent 404s for missing ESM chunks
  if (!window.Shopify) {
    window.Shopify = {};
  }
  try {
    Object.defineProperty(window.Shopify, 'featureAssets', {
      get: function() { return {}; },
      set: function(val) { /* ignore */ },
      configurable: true
    });
  } catch (e) {
    console.warn('[Cart Interceptor] Failed to define featureAssets override:', e);
  }

  var originalFetch = window.fetch;

  var isFlattened = window.location.pathname.indexOf('full%20download') !== -1 || 
                    window.location.pathname.indexOf('full download') !== -1 ||
                    window.location.pathname.indexOf('downloaded_site') !== -1 ||
                    window.location.pathname.indexOf('android_asset') !== -1 ||
                    window.location.pathname.indexOf('products_') !== -1 ||
                    window.location.pathname.indexOf('pages_') !== -1;

  var folderSeparator = isFlattened ? 'products_' : 'products/';
  var fileSuffix = isFlattened ? '/index.html' : '/';

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
  var productCachePromise = originalFetch(prefix + 'js/seed-data.json')
    .then(function(res) { return res.json(); })
    .then(function(data) {
      var cache = data.products || [];
      window.__rawjoyProductCache = cache;
      return cache;
    })
    .catch(function(err) {
      console.warn('[Cart Interceptor] Failed to load product cache:', err);
      return [];
    });

  var variantMapping = {
    "50655419892002": { "slug": "doggy-dental-mix", "variantName": "100gr" },
    "50655419924770": { "slug": "doggy-dental-mix", "variantName": "150gr" },
    "50655419957538": { "slug": "doggy-dental-mix", "variantName": "200gr" },
    "50657161773346": { "slug": "pet-meal-time-mix", "variantName": "100gr" },
    "50657161806114": { "slug": "pet-meal-time-mix", "variantName": "150gr" },
    "50657161838882": { "slug": "pet-meal-time-mix", "variantName": "200gr" },
    "50657163510050": { "slug": "cat-wellness-mix", "variantName": "100gr" },
    "50657163542818": { "slug": "cat-wellness-mix", "variantName": "150gr" },
    "50657163575586": { "slug": "cat-wellness-mix", "variantName": "200gr" },
    "50657166557474": { "slug": "cat-calming-formula", "variantName": "100gr" },
    "50657166590242": { "slug": "cat-calming-formula", "variantName": "150gr" },
    "50657166623010": { "slug": "cat-calming-formula", "variantName": "200gr" },
    "50657168458018": { "slug": "juicy-turkey-crunch", "variantName": "100gr" },
    "50657168490786": { "slug": "juicy-turkey-crunch", "variantName": "150gr" },
    "50657168523554": { "slug": "juicy-turkey-crunch", "variantName": "200gr" },
    "50657171210530": { "slug": "duck-soft-chews", "variantName": "100gr" },
    "50657171243298": { "slug": "duck-soft-chews", "variantName": "150gr" },
    "50657171276066": { "slug": "duck-soft-chews", "variantName": "200gr" },
    "50657172554018": { "slug": "chicken-pumpkin-pate", "variantName": "100gr" },
    "50657172586786": { "slug": "chicken-pumpkin-pate", "variantName": "150gr" },
    "50657172619554": { "slug": "chicken-pumpkin-pate", "variantName": "200gr" },
    "50657174913314": { "slug": "beef-spinach-stew", "variantName": "100gr" },
    "50657174946082": { "slug": "beef-spinach-stew", "variantName": "150gr" },
    "50657174978850": { "slug": "beef-spinach-stew", "variantName": "200gr" },
    "50657175535906": { "slug": "salmon-carrot-pate", "variantName": "100gr" },
    "50657175568674": { "slug": "salmon-carrot-pate", "variantName": "150gr" },
    "50657175601442": { "slug": "salmon-carrot-pate", "variantName": "200gr" },
    "50657178255650": { "slug": "rawjoy-soft-bar", "variantName": "100gr" },
    "50657178288418": { "slug": "rawjoy-soft-bar", "variantName": "150gr" },
    "50657178321186": { "slug": "rawjoy-soft-bar", "variantName": "200gr" },
    "50657185497378": { "slug": "crunchy-bone-treat", "variantName": "100gr" },
    "50657185530146": { "slug": "crunchy-bone-treat", "variantName": "150gr" },
    "50657185562914": { "slug": "crunchy-bone-treat", "variantName": "200gr" },
    "50657191035170": { "slug": "rawjoy-green-bar", "variantName": "100gr" },
    "50657191067938": { "slug": "rawjoy-green-bar", "variantName": "150gr" },
    "50657191100706": { "slug": "rawjoy-green-bar", "variantName": "200gr" },
    "50657195852066": { "slug": "mackerel-salmon-kibble", "variantName": "100gr" },
    "50657195884834": { "slug": "mackerel-salmon-kibble", "variantName": "150gr" },
    "50657195917602": { "slug": "mackerel-salmon-kibble", "variantName": "200gr" },
    "50657198539042": { "slug": "salmon-broccoli-crunch", "variantName": "100gr" },
    "50657198571810": { "slug": "salmon-broccoli-crunch", "variantName": "150gr" },
    "50657198604578": { "slug": "salmon-broccoli-crunch", "variantName": "200gr" },
    "50657199784226": { "slug": "salmon-rice-formula", "variantName": "100gr" },
    "50657199816994": { "slug": "salmon-rice-formula", "variantName": "150gr" },
    "50657199849762": { "slug": "salmon-rice-formula", "variantName": "200gr" },
    "50657202340130": { "slug": "lamb-quinoa-blend", "variantName": "100gr" },
    "50657202372898": { "slug": "lamb-quinoa-blend", "variantName": "150gr" },
    "50657202405666": { "slug": "lamb-quinoa-blend", "variantName": "200gr" },
    "50657212465442": { "slug": "venison-peas-recipe", "variantName": "100gr" },
    "50657212498210": { "slug": "venison-peas-recipe", "variantName": "150gr" },
    "50657212530978": { "slug": "venison-peas-recipe", "variantName": "200gr" },
    "50657215775010": { "slug": "juicy-turkey-stick", "variantName": "100gr" },
    "50657215807778": { "slug": "juicy-turkey-stick", "variantName": "150gr" },
    "50657215840546": { "slug": "juicy-turkey-stick", "variantName": "200gr" },
    "50657320403234": { "slug": "salmon-stick", "variantName": "100gr" },
    "50657320436002": { "slug": "salmon-stick", "variantName": "150gr" },
    "50657320468770": { "slug": "salmon-stick", "variantName": "200gr" },
    "50657320927522": { "slug": "chicken-herb-stick", "variantName": "100gr" },
    "50657320960290": { "slug": "chicken-herb-stick", "variantName": "150gr" },
    "50657320993058": { "slug": "chicken-herb-stick", "variantName": "200gr" },
    "50657359135010": { "slug": "fish-bone-treat", "variantName": "100gr" },
    "50657359167778": { "slug": "fish-bone-treat", "variantName": "150gr" },
    "50657359200546": { "slug": "fish-bone-treat", "variantName": "200gr" },
    "50657359560994": { "slug": "chicken-bone-treat", "variantName": "100gr" },
    "50657359593762": { "slug": "chicken-bone-treat", "variantName": "150gr" },
    "50657359626530": { "slug": "chicken-bone-treat", "variantName": "200gr" }
  };

  function isDummyBundleProduct(item) {
    if (!item) return false;
    var name = (item.name || item.title || '').toLowerCase();
    var slug = (item.slug || item.productId || '').toLowerCase();
    var id = String(item.id || '').toLowerCase();
    return name.indexOf('build your bundle') !== -1 || 
           name.indexOf('choose any 3') !== -1 ||
           slug.indexOf('build-your-bundle') !== -1 ||
           id.indexOf('build-your-bundle') !== -1;
  }

  // ---- LocalStorage Cart ----
  function calculateCartTotal(items) {
    var filteredItems = [];
    for (var i = 0; i < items.length; i++) {
      var item = items[i];
      if (!isDummyBundleProduct(item)) {
        filteredItems.push(item);
      }
    }
    var total = 0;
    for (var i = 0; i < filteredItems.length; i++) {
      var item = filteredItems[i];
      var price = item.price || 0;
      total += price * (item.quantity || 1);
    }
    return Math.round(total);
  }

  function getCart() {
    try {
      var data = localStorage.getItem('rawjoy_cart_hybrid') || '{"items":[]}';
      var parsed = JSON.parse(data);
      
      // Filter out dummy/virtual bundle products
      var filteredItems = [];
      for (var i = 0; i < parsed.items.length; i++) {
        var item = parsed.items[i];
        if (!isDummyBundleProduct(item)) {
          filteredItems.push(item);
        }
      }
      parsed.items = filteredItems;

      var total = calculateCartTotal(parsed.items);
      return { items: parsed.items, total: total };
    } catch (e) {
      return { items: [], total: 0 };
    }
  }

  function saveCart(cart) {
    // Also clean before saving just in case
    if (cart && cart.items) {
      var filteredItems = [];
      for (var i = 0; i < cart.items.length; i++) {
        var item = cart.items[i];
        if (!isDummyBundleProduct(item)) {
          filteredItems.push(item);
        }
      }
      cart.items = filteredItems;
    }
    localStorage.setItem('rawjoy_cart_hybrid', JSON.stringify(cart));
  }

  function getTotalItems() {
    var cart = getCart();
    var count = 0;
    for (var i = 0; i < cart.items.length; i++) {
      if (!isDummyBundleProduct(cart.items[i])) {
        count += cart.items[i].quantity || 1;
      }
    }
    return count;
  }

  // ---- DOM Product Extraction ----
  function extractProduct(variantId) {
    var name = '', slug = '', price = 0, image = '';
    var variantName = null;

    // Check if variantId is a slug or matches a product in the cache
    var cache = window.__rawjoyProductCache || [];
    var cachedProduct = null;
    
    // First, try lookup in cache by slug directly
    for (var i = 0; i < cache.length; i++) {
      if (cache[i].slug === variantId || cache[i].id === variantId) {
        cachedProduct = cache[i];
        break;
      }
    }
    
    // If not found, check variant mapping
    if (!cachedProduct) {
      var mapped = variantMapping[variantId];
      if (mapped) {
        var mappedSlug = mapped.slug;
        variantName = mapped.variantName || null;
        for (var i = 0; i < cache.length; i++) {
          if (cache[i].slug === mappedSlug) {
            cachedProduct = cache[i];
            break;
          }
        }
      }
    }

    if (cachedProduct) {
      name = cachedProduct.name;
      slug = cachedProduct.slug;
      price = cachedProduct.price;
      image = cachedProduct.mainImage || (cachedProduct.images && cachedProduct.images[0]) || '';
    }

    // Now try DOM extraction as an override / fallback for variant name etc.
    var element = document.querySelector('input[name="id"][value="' + variantId + '"]') ||
                  document.querySelector('select[name="id"] option[value="' + variantId + '"]') ||
                  document.querySelector('option[value="' + variantId + '"]');
    
    if (element) {
      var form = element.closest('form') || element.closest('product-bundle-selection') || element.closest('product-card') || element.closest('.product-card');
      if (form) {
        var quickAdd = form.closest('quick-add-component');
        var card = form.closest('product-card') || form.closest('.product-card') || form;
        var dialog = form.closest('dialog');
        var section = form.closest('.shopify-section');

        // Extract from DOM
        var domName = '', domSlug = '', domPrice = 0, domImage = '';

        if (quickAdd) {
          domName = quickAdd.getAttribute('data-product-title') || '';
          var pUrl = quickAdd.getAttribute('data-product-url') || '';
          var m = pUrl.match(/products\/([^/?#]+)/);
          if (m) domSlug = m[1];
        }

        if (card) {
          if (!domName) {
            var titleEl = card.querySelector('.product-card__title .reversed-link__text');
            if (titleEl) domName = titleEl.textContent.trim();
          }
          if (!domSlug) {
            var link = card.querySelector('a[href*="products/"]');
            if (link) {
              var href = link.getAttribute('href');
              var hm = href.match(/products\/([^/?#]+)/);
              if (hm) domSlug = hm[1];
            }
          }
          var priceEl = card.querySelector('product-price .price__regular .price') ||
                        card.querySelector('product-price .price');
          if (priceEl) {
            domPrice = parseFloat(priceEl.textContent.replace(/[^0-9.,]/g, '').replace(',', '.')) || 0;
          }
          var imgEl = card.querySelector('img.product-card-main-image') ||
                      card.querySelector('.product-card__image img');
          if (imgEl) {
            domImage = imgEl.getAttribute('src') || '';
          }
        }

        // Apply DOM values if they were successfully found
        if (domName) name = domName;
        if (domSlug) slug = domSlug;
        if (domPrice) price = domPrice;
        if (domImage) image = domImage;

        // Try extracting variant name from radio buttons
        if (!variantName) {
          var container = dialog || card || section || document;
          var radio = container.querySelector('input[type="radio"]:checked');
          if (radio) variantName = radio.value || null;
        }
      }
    }

    if (!name && !slug) {
      console.warn('[Cart] Could not extract product for variant:', variantId);
      return null;
    }

    // Final variant price resolution using the resolved variantName
    if (cachedProduct && variantName && cachedProduct.variants) {
      for (var v = 0; v < cachedProduct.variants.length; v++) {
        if (cachedProduct.variants[v].name === variantName) {
          price = cachedProduct.variants[v].price;
          break;
        }
      }
    }

    console.log('[Cart] Extracted:', name, slug, '$' + price);
    return { id: slug || String(variantId), name: name || slug, slug: slug, price: price, image: image, variant: variantName };
  }

  // ---- Cart Drawer HTML ----
  function buildSectionsHTML(cart, sectionId) {
    if (cart && cart.items) {
      var filteredItems = [];
      for (var idx = 0; idx < cart.items.length; idx++) {
        var item = cart.items[idx];
        if (!isDummyBundleProduct(item)) {
          filteredItems.push(item);
        }
      }
      cart.items = filteredItems;
    }

    var totalItems = 0;
    for (var k = 0; k < cart.items.length; k++) {
      totalItems += cart.items[k].quantity || 1;
    }
    
    var originalTotal = 0;
    for (var i = 0; i < cart.items.length; i++) {
      var item = cart.items[i];
      originalTotal += item.price * item.quantity;
    }
    var totalStr = '$' + originalTotal.toFixed(2);

    var rows = '';
    var depth = window.location.pathname.split('/').filter(Boolean).length;
    var prefix = getDepthPrefix();

    var isDialogOpen = false;
    try {
      var existingDialog = document.getElementById('cart-drawer-dialog');
      if (existingDialog && (existingDialog.open || existingDialog.hasAttribute('open'))) {
        isDialogOpen = true;
      }
    } catch(e) {}

    for (var i = 0; i < cart.items.length; i++) {
      var item = cart.items[i];
      var isSale = item.name.toLowerCase().indexOf('salmon stick') !== -1 || item.name.toLowerCase().indexOf('cat calming') !== -1;
      var comparePrice = isSale ? item.price * 1.4545 : null;
      
      var priceFormatted = '$' + (item.price || 0).toFixed(2);
      var compareFormatted = comparePrice ? '$' + comparePrice.toFixed(2) : null;

      var imgPath = getLocalProductImage(item, prefix);

      rows += '<div class="cart-item-card" ref="cartItemRows[]" data-line="' + (i+1) + '">' +
        '<div class="cart-item-image-wrapper">' +
        '<a href="' + prefix + folderSeparator + item.slug + fileSuffix + '" tabindex="-1">' +
        '<img src="' + imgPath + '" alt="' + item.name + '" loading="lazy">' +
        '</a></div>' +
        '<div class="cart-item-details">' +
        '<a class="cart-item-title reversed-link" href="' + prefix + folderSeparator + item.slug + fileSuffix + '"><span class="reversed-link__text">' + item.name + '</span></a>' +
        (item.variant ? '<p class="cart-item-variant">' + item.variant + '</p>' : '') +
        '<div class="cart-item-actions">' +
        '<div class="qty-pill">' +
        '<button type="button" class="qty-btn" onclick="window.updateCartQty(' + (i+1) + ', ' + (item.quantity - 1) + ')">-</button>' +
        '<span class="qty-val">' + item.quantity + '</span>' +
        '<button type="button" class="qty-btn" onclick="window.updateCartQty(' + (i+1) + ', ' + (item.quantity + 1) + ')">+</button>' +
        '</div>' +
        '<a class="remove-link" onclick="window.updateCartQty(' + (i+1) + ', 0); return false;">Remove</a>' +
        '</div></div>' +
        '<div class="cart-item-price-wrapper">' +
        '<span class="' + (isSale ? 'sale-price' : 'normal-price') + '">' + priceFormatted + '</span>' + (compareFormatted ? '<span class="compare-price">' + compareFormatted + '</span>' : '') +
        '</div></div>';
    }

    var isEmpty = cart.items.length === 0;

    // Shipping goal
    var threshold = 50;
    var remaining = threshold - originalTotal;
    var shippingText = '';
    var progressPercent = Math.min((originalTotal / threshold) * 100, 100);
    if (remaining > 0) {
      var remStr = '$' + remaining.toFixed(2);
      shippingText = 'Spend <span style="font-weight: 700; color: #008a5b;">' + remStr + '</span> more to reach free shipping!';
    } else {
      shippingText = "You've unlocked free shipping!";
    }

    // Recommended products
    var inCartSlugs = cart.items.map(function(item) { return item.slug || item.productId; });
    var recommendedList = [
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

    var filteredRecommended = recommendedList.filter(function(p) {
      return inCartSlugs.indexOf(p.slug) === -1;
    });

    var recommendedCards = '';
    for (var j = 0; j < filteredRecommended.length; j++) {
      var rp = filteredRecommended[j];
      var rpPriceStr = '$' + rp.price.toFixed(2);
      var rpCompareStr = rp.comparePrice ? '$' + rp.comparePrice.toFixed(2) : null;
      var rpImg = rp.image ? (prefix + rp.image.replace('products/', folderSeparator)) : '';
      
      recommendedCards += '<div class="complete-look-card">' +
        '<div class="complete-look-img-wrapper">' +
        '<img src="' + rpImg + '" alt="' + rp.name + '" loading="lazy">' +
        '</div>' +
        '<div class="complete-look-info">' +
        '<span class="complete-look-name">' + rp.name + '</span>' +
        '<div class="complete-look-price-row">' +
        '<span class="complete-look-price ' + (rpCompareStr ? 'sale' : '') + '">' + rpPriceStr + '</span>' +
        (rpCompareStr ? '<span class="complete-look-compare">' + rpCompareStr + '</span>' : '') +
        (rpCompareStr ? '<span class="complete-look-badge">Sale</span>' : '') +
        '</div></div>' +
        '<button type="button" class="complete-look-add-btn" onclick="window.addRecommendedToCart(\'' + rp.id + '\', this)">' +
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>' +
        '</button></div>';
    }

    var completeLookSection = '';
    if (filteredRecommended.length > 0) {
      completeLookSection = '<div class="complete-look-section">' +
        '<div class="complete-look-header">' +
        '<span class="complete-look-title">Complete The Look</span>' +
        '<div class="complete-look-arrows">' +
        '<button type="button" class="arrow-btn" onclick="var el = this.closest(\'.complete-look-section\').querySelector(\'.complete-look-list\'); el.scrollBy({left: -150, behavior: \'smooth\'});">&lt;</button>' +
        '<button type="button" class="arrow-btn" onclick="var el = this.closest(\'.complete-look-section\').querySelector(\'.complete-look-list\'); el.scrollBy({left: 150, behavior: \'smooth\'});">&gt;</button>' +
        '</div>' +
        '</div>' +
        '<div class="complete-look-list">' +
        recommendedCards +
        '</div>' +
        '</div>';
    }

    return '<div class="shopify-section shopify-section-group-overlay-group" id="shopify-section-' + sectionId + '">' +
      '<style>' +
      '  .shopify-section-group-overlay-group, ' +
      '  [id^="shopify-section-"][id$="-drawer"] {' +
      '    position: relative !important;' +
      '    z-index: 999999 !important;' +
      '  }' +
      '  #cart-drawer-dialog {' +
      '    max-width: 480px !important;' +
      '    width: 100% !important;' +
      '    background: #ffffff !important;' +
      '    font-family: Poppins, sans-serif !important;' +
      '    z-index: 999999 !important;' +
      '  }' +
      '  .cart-drawer__inner {' +
      '    padding: 0 !important;' +
      '    display: flex;' +
      '    flex-direction: column;' +
      '    height: 100%;' +
      '  }' +
      '  .cart-items-component {' +
      '    display: flex;' +
      '    flex-direction: column;' +
      '    height: 100%;' +
      '  }' +
      '  .cart-drawer__header {' +
      '    padding: 20px !important;' +
      '    border-bottom: 1px solid #f0f0f0 !important;' +
      '    display: flex !important;' +
      '    align-items: center !important;' +
      '    justify-content: space-between !important;' +
      '  }' +
      '  .cart-drawer__heading {' +
      '    font-family: Poppins, sans-serif !important;' +
      '    font-weight: 700 !important;' +
      '    font-size: 2.2rem !important;' +
      '    color: #000000 !important;' +
      '    margin: 0 !important;' +
      '  }' +
      '  .cart-drawer__content {' +
      '    flex: 1 !important;' +
      '    overflow-y: auto !important;' +
      '    padding: 0 !important;' +
      '  }' +
      '  .cart-item-card {' +
      '    display: flex;' +
      '    align-items: center;' +
      '    padding: 16px 20px;' +
      '    border-bottom: 1px solid #f6f6f6;' +
      '    gap: 16px;' +
      '    background: #ffffff;' +
      '    transition: background-color 0.2s ease;' +
      '  }' +
      '  .cart-item-card:hover {' +
      '    background: #fafafa;' +
      '  }' +
      '  .cart-item-image-wrapper {' +
      '    width: 90px;' +
      '    height: 90px;' +
      '    border-radius: 12px;' +
      '    background: #f4f4f4;' +
      '    display: flex;' +
      '    align-items: center;' +
      '    justify-content: center;' +
      '    overflow: hidden;' +
      '    flex-shrink: 0;' +
      '  }' +
      '  .cart-item-image-wrapper img {' +
      '    max-width: 80%;' +
      '    max-height: 80%;' +
      '    object-fit: contain;' +
      '  }' +
      '  .cart-item-details {' +
      '    flex: 1;' +
      '    display: flex;' +
      '    flex-direction: column;' +
      '    gap: 4px;' +
      '    text-align: left;' +
      '  }' +
      '  .cart-item-title {' +
      '    font-size: 1.5rem;' +
      '    font-weight: 600;' +
      '    color: #000000;' +
      '    line-height: 1.3;' +
      '  }' +
      '  .cart-item-variant {' +
      '    font-size: 1.2rem;' +
      '    color: #888888;' +
      '  }' +
      '  .cart-item-actions {' +
      '    display: flex;' +
      '    align-items: center;' +
      '    margin-top: 8px;' +
      '    gap: 12px;' +
      '  }' +
      '  .qty-pill {' +
      '    border: 1px solid #e0e0e0;' +
      '    border-radius: 20px;' +
      '    display: inline-flex;' +
      '    align-items: center;' +
      '    padding: 3px 12px;' +
      '    gap: 12px;' +
      '    background: #ffffff;' +
      '  }' +
      '  .qty-btn {' +
      '    background: none;' +
      '    border: none;' +
      '    font-size: 1.6rem;' +
      '    font-weight: 700;' +
      '    cursor: pointer;' +
      '    color: #000000;' +
      '    padding: 0 4px;' +
      '    display: flex;' +
      '    align-items: center;' +
      '    justify-content: center;' +
      '    user-select: none;' +
      '  }' +
      '  .qty-btn:hover {' +
      '    color: #f05230;' +
      '  }' +
      '  .qty-val {' +
      '    font-weight: 600;' +
      '    font-size: 1.3rem;' +
      '    min-width: 16px;' +
      '    text-align: center;' +
      '  }' +
      '  .remove-link {' +
      '    color: #777777;' +
      '    font-size: 1.2rem;' +
      '    text-decoration: underline;' +
      '    cursor: pointer;' +
      '    font-weight: 500;' +
      '  }' +
      '  .remove-link:hover {' +
      '    color: #000000;' +
      '  }' +
      '  .cart-item-price-wrapper {' +
      '    display: flex;' +
      '    flex-direction: column;' +
      '    align-items: flex-end;' +
      '    justify-content: center;' +
      '    min-width: 70px;' +
      '  }' +
      '  .sale-price {' +
      '    font-size: 1.5rem;' +
      '    font-weight: 700;' +
      '    color: #f05230;' +
      '  }' +
      '  .normal-price {' +
      '    font-size: 1.5rem;' +
      '    font-weight: 700;' +
      '    color: #000000;' +
      '  }' +
      '  .compare-price {' +
      '    font-size: 1.3rem;' +
      '    text-decoration: line-through;' +
      '    color: #999999;' +
      '    margin-top: 2px;' +
      '  }' +
      '  .complete-look-section {' +
      '    background: #fafafa;' +
      '    border-top: 1px solid #eeeeee;' +
      '    padding: 20px 0 10px 0;' +
      '  }' +
      '  .complete-look-header {' +
      '    display: flex;' +
      '    justify-content: space-between;' +
      '    align-items: center;' +
      '    padding: 0 20px 12px 20px;' +
      '  }' +
      '  .complete-look-title {' +
      '    font-size: 1.6rem;' +
      '    font-weight: 700;' +
      '    color: #000000;' +
      '    margin: 0;' +
      '  }' +
      '  .complete-look-arrows {' +
      '    display: flex;' +
      '    gap: 8px;' +
      '  }' +
      '  .arrow-btn {' +
      '    background: none;' +
      '    border: none;' +
      '    cursor: pointer;' +
      '    font-size: 1.6rem;' +
      '    font-weight: 700;' +
      '    color: #000000;' +
      '    padding: 4px;' +
      '    opacity: 0.6;' +
      '    transition: opacity 0.2s;' +
      '  }' +
      '  .arrow-btn:hover {' +
      '    opacity: 1;' +
      '  }' +
      '  .complete-look-list {' +
      '    display: flex;' +
      '    gap: 12px;' +
      '    padding: 0 20px 10px 20px;' +
      '    overflow-x: auto;' +
      '    scrollbar-width: none;' +
      '  }' +
      '  .complete-look-list::-webkit-scrollbar {' +
      '    display: none;' +
      '  }' +
      '  .complete-look-card {' +
      '    background: #ffffff;' +
      '    border: 1px solid #eeeeee;' +
      '    border-radius: 12px;' +
      '    padding: 12px;' +
      '    display: flex;' +
      '    align-items: center;' +
      '    gap: 12px;' +
      '    min-width: 250px;' +
      '    flex-shrink: 0;' +
      '    box-shadow: 0 2px 6px rgba(0,0,0,0.02);' +
      '  }' +
      '  .complete-look-img-wrapper {' +
      '    width: 60px;' +
      '    height: 60px;' +
      '    border-radius: 8px;' +
      '    background: #f5f5f5;' +
      '    display: flex;' +
      '    align-items: center;' +
      '    justify-content: center;' +
      '    overflow: hidden;' +
      '    flex-shrink: 0;' +
      '  }' +
      '  .complete-look-img-wrapper img {' +
      '    max-width: 85%;' +
      '    max-height: 85%;' +
      '    object-fit: contain;' +
      '  }' +
      '  .complete-look-info {' +
      '    flex: 1;' +
      '    text-align: left;' +
      '    display: flex;' +
      '    flex-direction: column;' +
      '  }' +
      '  .complete-look-name {' +
      '    font-size: 1.35rem;' +
      '    font-weight: 600;' +
      '    color: #000000;' +
      '    line-height: 1.3;' +
      '  }' +
      '  .complete-look-price-row {' +
      '    display: flex;' +
      '    align-items: center;' +
      '    gap: 6px;' +
      '    margin-top: 4px;' +
      '  }' +
      '  .complete-look-price {' +
      '    font-size: 1.3rem;' +
      '    font-weight: 700;' +
      '    color: #000000;' +
      '  }' +
      '  .complete-look-price.sale {' +
      '    color: #f05230;' +
      '  }' +
      '  .complete-look-compare {' +
      '    font-size: 1.15rem;' +
      '    text-decoration: line-through;' +
      '    color: #999999;' +
      '  }' +
      '  .complete-look-badge {' +
      '    background: #ffebe7;' +
      '    color: #f05230;' +
      '    font-size: 1rem;' +
      '    font-weight: 700;' +
      '    padding: 1px 6px;' +
      '    border-radius: 4px;' +
      '    margin-left: 6px;' +
      '  }' +
      '  .complete-look-add-btn {' +
      '    width: 36px;' +
      '    height: 36px;' +
      '    border-radius: 50%;' +
      '    background: #000000;' +
      '    color: #ffffff;' +
      '    display: flex;' +
      '    align-items: center;' +
      '    justify-content: center;' +
      '    border: none;' +
      '    cursor: pointer;' +
      '    transition: transform 0.2s, background-color 0.2s;' +
      '    flex-shrink: 0;' +
      '  }' +
      '  .complete-look-add-btn:hover {' +
      '    background: #f05230;' +
      '    transform: scale(1.05);' +
      '  }' +
      '  .premium-cart-footer {' +
      '    background: #000000 !important;' +
      '    padding: 24px 20px !important;' +
      '    color: #ffffff !important;' +
      '    border-top: none !important;' +
      '    font-family: Poppins, sans-serif !important;' +
      '  }' +
      '  .footer-price-section {' +
      '    display: flex;' +
      '    justify-content: space-between;' +
      '    align-items: flex-start;' +
      '    margin-bottom: 12px;' +
      '  }' +
      '  .footer-total-label {' +
      '    font-size: 1.3rem;' +
      '    color: #b0b0b0;' +
      '    text-transform: capitalize;' +
      '    font-weight: 500;' +
      '  }' +
      '  .footer-total-price {' +
      '    font-size: 3.2rem;' +
      '    font-weight: 700;' +
      '    color: #ffffff;' +
      '    margin-top: 4px;' +
      '  }' +
      '  .footer-actions {' +
      '    display: flex;' +
      '    align-items: center;' +
      '    gap: 8px;' +
      '    margin-top: 4px;' +
      '  }' +
      '  .footer-icon-btn {' +
      '    width: 36px;' +
      '    height: 36px;' +
      '    border-radius: 50%;' +
      '    background: #222222;' +
      '    color: #ffffff;' +
      '    display: flex;' +
      '    align-items: center;' +
      '    justify-content: center;' +
      '    border: none;' +
      '    cursor: pointer;' +
      '    transition: background-color 0.2s;' +
      '  }' +
      '  .footer-icon-btn:hover {' +
      '    background: #333333;' +
      '  }' +
      '  .footer-disclaimer {' +
      '    font-size: 1.15rem;' +
      '    color: #888888;' +
      '    line-height: 1.4;' +
      '    margin-bottom: 18px;' +
      '    text-align: right;' +
      '  }' +
      '  .footer-buttons-row {' +
      '    display: flex;' +
      '    gap: 12px;' +
      '  }' +
      '  .footer-btn {' +
      '    flex: 1;' +
      '    border-radius: 30px;' +
      '    padding: 12px 0;' +
      '    font-size: 1.4rem;' +
      '    font-weight: 600;' +
      '    text-align: center;' +
      '    text-decoration: none !important;' +
      '    cursor: pointer;' +
      '    transition: all 0.2s ease;' +
      '    display: inline-block;' +
      '    box-sizing: border-box;' +
      '  }' +
      '  .footer-btn-outline {' +
      '    background: transparent;' +
      '    color: #ffffff;' +
      '    border: 1.5px solid #ffffff;' +
      '  }' +
      '  .footer-btn-outline:hover {' +
      '    background: #222222;' +
      '  }' +
      '  .footer-btn-filled {' +
      '    background: #ffffff;' +
      '    color: #000000;' +
      '    border: 1.5px solid #ffffff;' +
      '  }' +
      '  .footer-btn-filled:hover {' +
      '    background: #f0f0f0;' +
      '  }' +
      '  .bundle-discount-banner {' +
      '    background: #e8f5e9 !important;' +
      '    border: 1px solid #c8e6c9 !important;' +
      '    border-radius: 12px !important;' +
      '    padding: 12px 16px !important;' +
      '    margin: 16px 20px !important;' +
      '    display: flex !important;' +
      '    align-items: center !important;' +
      '    gap: 12px !important;' +
      '  }' +
      '  .bundle-banner-icon {' +
      '    font-size: 2.2rem !important;' +
      '  }' +
      '  .bundle-banner-text {' +
      '    display: flex !important;' +
      '    flex-direction: column !important;' +
      '    text-align: left !important;' +
      '  }' +
      '  .bundle-banner-text strong {' +
      '    color: #2e7d32 !important;' +
      '    font-size: 1.4rem !important;' +
      '    font-weight: 700 !important;' +
      '  }' +
      '  .bundle-banner-text span {' +
      '    color: #4caf50 !important;' +
      '    font-size: 1.2rem !important;' +
      '    font-weight: 500 !important;' +
      '    margin-top: 2px !important;' +
      '  }' +
      '  .bundle-promo-banner {' +
      '    background: #fff8e1 !important;' +
      '    border: 1px solid #ffe082 !important;' +
      '    border-radius: 12px !important;' +
      '    padding: 12px 16px !important;' +
      '    margin: 16px 20px !important;' +
      '    text-align: left !important;' +
      '    color: #b78103 !important;' +
      '    font-size: 1.25rem !important;' +
      '    font-weight: 500 !important;' +
      '    line-height: 1.4 !important;' +
      '  }' +
      '  .bundle-promo-banner strong {' +
      '    color: #e65100 !important;' +
      '    font-weight: 700 !important;' +
      '  }' +
      '  .bundle-badge {' +
      '    background: #e8f5e9 !important;' +
      '    color: #2e7d32 !important;' +
      '    font-size: 1.1rem !important;' +
      '    font-weight: 700 !important;' +
      '    padding: 2px 8px !important;' +
      '    border-radius: 4px !important;' +
      '    display: inline-block !important;' +
      '    margin-top: 4px !important;' +
      '    width: fit-content !important;' +
      '  }' +
      '</style>' +
      '<link href="' + prefix + 'css/cart-drawer.css" media="all" rel="stylesheet">' +
      '<link href="' + prefix + 'css/cart-modules.css" media="all" rel="stylesheet">' +
      '<script src="' + prefix + 'js/cart-drawer.js" type="module"></script>' +
      '<script src="' + prefix + 'js/cart-items.js" type="module"></script>' +
      '<script src="' + prefix + 'js/cart-shipping.js" type="module"></script>' +
      '<script src="' + prefix + 'js/product-recommendations.js" type="module"></script>' +
      '<cart-drawer-component auto-open="" class="cart-drawer" id="CartDrawer">' +
      '<dialog ' + (isDialogOpen ? 'open="" ' : '') + 'class="dialog dialog--drawer dialog--cart-drawer dialog--drawer-right overflow-hidden" id="cart-drawer-dialog" ref="dialog" scroll-lock="">' +
      '<div class="cart-drawer__inner">' +
      '<cart-items-component class="cart-items-component" data-section-id="' + sectionId + '">' +
      '<span class="visually-hidden" ref="cartItemCount" style="display:none;">' + totalItems + '</span>' +
      '<span class="cart-bubble__text-count" style="display:none;">' + totalItems + '</span>' +
      '<div class="cart-drawer__header relative flex items-center justify-between gap-2" id="cart-drawer-header">' +
      '<span class="cart-drawer__heading cart__heading relative h3" style="display:inline-flex; align-items:baseline;">Your cart' +
      '<sup style="font-size: 0.6em; font-weight: 700; margin-left: 2px; vertical-align: super; top: -0.5em; position: relative;">' + totalItems + '</sup>' +
      '</span>' +
      '<button class="cart-drawer__close dialog__close shrink-0" on:click="cart-drawer-component/close">' +
      '<span class="icon icon--close icon--large"><svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M0 0H20V20H0V0z" fill="none" height="256" width="256"></path><path d="M15.625 4.375L4.375 15.625" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="var(--icon-stroke-width, 2)"></path><path d="M15.625 15.625L4.375 4.375" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="var(--icon-stroke-width, 2)"></path></svg></span>' +
      '</button>' +
      '</div>' +
      '<div class="cart-drawer__shipping-goal" style="padding: 15px 20px; font-family: Poppins, sans-serif; font-size: 1.4rem;">' +
      '  <div style="color: #008a5b; margin-bottom: 8px; font-weight: 500;">' + shippingText + '</div>' +
      '  <div style="background: #e8e8e8; border-radius: 10px; height: 6px; overflow: hidden; width: 100%;">' +
      '    <div style="background: #008a5b; width: ' + progressPercent + '%; height: 100%; transition: width 0.3s ease; border-radius: 10px;"></div>' +
      '  </div>' +
      '</div>' +
      '<div class="cart-drawer__content">' +
      (isEmpty ? '<div class="cart-drawer__empty text-center"><p>Your cart is empty</p></div>' : rows) +
      (!isEmpty ? completeLookSection : '') +
      '</div>' +
      (!isEmpty ? 
      '<div class="premium-cart-footer">' +
      '  <div class="footer-price-section">' +
      '    <div>' +
      '      <div class="footer-total-label">Estimated total</div>' +
      '      <div class="footer-total-price">' + totalStr + '</div>' +
      '    </div>' +
      '    <div class="footer-actions">' +
      '      <button type="button" class="footer-icon-btn">' +
      '        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 1 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>' +
      '      </button>' +
      '      <button type="button" class="footer-icon-btn">' +
      '        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="16.5" y1="9.4" x2="7.5" y2="4.21"></line><polygon points="12 22.08 12 12 3 6.92 3 17.08 12 22.08"></polygon><polygon points="12 12 21 6.92 21 17.08 12 22.08"></polygon><polygon points="12 2 3 6.92 12 12 21 6.92 12 2"></polygon><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>' +
      '      </button>' +
      '    </div>' +
      '  </div>' +
      '  <div class="footer-disclaimer">Taxes, discounts and shipping calculated at checkout.</div>' +
      '  <div class="footer-buttons-row">' +
      '    <a class="footer-btn footer-btn-outline" href="' + prefix + 'cart/index.html">View Cart</a>' +
      '    <a class="footer-btn footer-btn-filled" href="' + prefix + 'pages/checkout/index.html">Check Out</a>' +
      '  </div>' +
      '</div>' : '') +
      '</cart-items-component>' +
      '</div>' +
      '</dialog>' +
      '</cart-drawer-component>' +
      '</div>';
  }

  // Global helper functions exposed for the custom cart buttons
  window.updateCartQty = function(line, newQty) {
    console.log('[Cart Interceptor] updateCartQty line:', line, 'qty:', newQty);
    var event = new CustomEvent("quantity-selector:update", {
      bubbles: true,
      detail: { quantity: newQty, cartLine: line }
    });
    document.dispatchEvent(event);
  };

  window.addRecommendedToCart = function(productId, btn) {
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<span style="font-size: 1.2rem;">...</span>';
    }
    
    // Determine the product page URL dynamically
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
          console.log('[DEBUG resolveUrl] Input relUrl:', relUrl, 'baseUrl:', baseUrl);
          if (!relUrl || relUrl.startsWith('http:') || relUrl.startsWith('https:') || relUrl.startsWith('data:')) {
            var res = relUrl;
            console.log('[DEBUG resolveUrl] Output (no-change):', res);
            return res;
          }
          if (relUrl.startsWith('/')) {
            var subfolderPrefix = getSubfolderPrefix();
            var res = relUrl;
            if (subfolderPrefix !== '/') {
              if (!relUrl.toLowerCase().startsWith(subfolderPrefix.toLowerCase())) {
                res = subfolderPrefix + relUrl.substring(1);
              }
            }
            console.log('[DEBUG resolveUrl] Output (starts-with-/):', res);
            return res;
          }
          try {
            var res = new URL(relUrl, new URL(baseUrl, window.location.href)).toString();
            console.log('[DEBUG resolveUrl] Output (resolved):', res);
            return res;
          } catch(e) {
            console.log('[DEBUG resolveUrl] Output (error):', relUrl, e);
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
          
          // Keep the cart drawer open behind the Quick Add modal (prevent flickering/disappearing)
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

  // ---- Update Cart Count Badges ----
  function updateCartBadges(customCount) {
    var count = typeof customCount === 'number' ? customCount : getTotalItems();
    var els = document.querySelectorAll('.cart-bubble__text-count');
    for (var i = 0; i < els.length; i++) {
      els[i].textContent = count;
    }
    var carts = document.querySelectorAll('cart-count');
    for (var j = 0; j < carts.length; j++) {
      if (count > 0) carts[j].classList.remove('hidden');
      else carts[j].classList.add('hidden');
    }
  }

  window.updateCartBadges = updateCartBadges;

  function injectCartHtml(container, html, sectionId) {
    // Always ensure cart drawer styles are present in the document head
    var tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;
    var newStyle = tempDiv.querySelector('style');
    if (newStyle) {
      var existingCartStyle = document.getElementById('cart-drawer-injected-styles');
      if (existingCartStyle) {
        existingCartStyle.textContent = newStyle.textContent;
      } else {
        var styleEl = document.createElement('style');
        styleEl.id = 'cart-drawer-injected-styles';
        styleEl.textContent = newStyle.textContent;
        document.head.appendChild(styleEl);
      }
    }

    var existingDialog = document.getElementById('cart-drawer-dialog');
    if (existingDialog) {
      var newInner = tempDiv.querySelector('.cart-drawer__inner');
      if (newInner) {
        var existingInner = existingDialog.querySelector('.cart-drawer__inner');
        if (existingInner) {
          existingInner.innerHTML = newInner.innerHTML;
        } else {
          existingDialog.innerHTML = newInner.outerHTML;
        }
        var newCountEl = tempDiv.querySelector('.visually-hidden[ref="cartItemCount"]');
        var newBubbleEl = tempDiv.querySelector('.cart-bubble__text-count');
        if (newCountEl) {
          var existingCountEl = existingDialog.querySelector('.visually-hidden[ref="cartItemCount"]');
          if (existingCountEl) existingCountEl.textContent = newCountEl.textContent;
        }
        if (newBubbleEl) {
          var existingBubbleEl = existingDialog.querySelector('.cart-bubble__text-count');
          if (existingBubbleEl) existingBubbleEl.textContent = newBubbleEl.textContent;
        }
        console.log('[Cart Interceptor] Updated cart drawer content in-place.');
        return;
      }
    }
    container.outerHTML = html;
  }

  function updateAndInjectCart() {
    var cartDrawer = document.getElementById('CartDrawer');
    var container = document.getElementById('shopify-section-sections--26013853417762__cart-drawer') || 
                    document.querySelector('.shopify-section-group-overlay-group[id*="cart-drawer"]') || 
                    (cartDrawer ? cartDrawer.closest('.shopify-section') : null);
    if (!container) {
      console.warn('[Cart] Cart drawer container not found in DOM.');
      return;
    }
    var sectionId = container.id.replace('shopify-section-', '');
    
    if (window.DB && window.DB.cart) {
      window.DB.cart.get().then(function(c) {
        var html = buildSectionsHTML(c, sectionId);
        injectCartHtml(container, html, sectionId);
      }).catch(function(e) {
        console.error('[Cart] DB get cart error:', e);
        var cart = getCart();
        var html = buildSectionsHTML(cart, sectionId);
        injectCartHtml(container, html, sectionId);
      });
    } else {
      var cart = getCart();
      var html = buildSectionsHTML(cart, sectionId);
      injectCartHtml(container, html, sectionId);
    }
  }

  window.updateAndInjectCart = updateAndInjectCart;

  // ---- Helper functions for search ----
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

  function escapeHtml(unsafe) {
    return (unsafe || '')
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
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
  window.getLocalProductImage = getLocalProductImage;

  async function handlePredictiveSearch(url) {
    var urlObj;
    try {
      var absoluteUrl = url.indexOf('http') === 0 || url.indexOf('//') === 0 ? url : window.location.origin + (url.indexOf('/') === 0 ? '' : '/') + url;
      urlObj = new URL(absoluteUrl);
    } catch (e) {
      urlObj = new URL(window.location.origin + '/' + url);
    }
    var searchTerm = urlObj.searchParams.get('q') || '';
    var sectionId = urlObj.searchParams.get('section_id') || 'sections--26013853450530__header';
    var limit = parseInt(urlObj.searchParams.get('resources[limit]') || '3', 10);

    console.log('[Search] Offline search for:', searchTerm, 'limit:', limit, 'sectionId:', sectionId);

    var products = [];
    if (window.DB && window.DB.products) {
      try {
        products = await window.DB.products.getAll();
      } catch(e) {
        console.warn('[Search] DB products getAll failed:', e);
      }
    }
    
    if (!products || products.length === 0) {
      var prefix = getDepthPrefix();
      try {
        var res = await originalFetch(prefix + 'js/seed-data.json');
        var seedData = await res.json();
        products = seedData.products || [];
        console.log('[Search] Loaded products from seed-data.json fallback:', products.length);
      } catch(e) {
        console.error('[Search] Failed to fetch fallback seed data:', e);
      }
    }

    var matched = [];
    var qLower = searchTerm.trim().toLowerCase();
    if (qLower) {
      for (var i = 0; i < products.length; i++) {
        var p = products[i];
        var nameMatches = (p.name || '').toLowerCase().indexOf(qLower) !== -1;
        var descMatches = (p.description || '').toLowerCase().indexOf(qLower) !== -1;
        var catMatches = (p.category || '').toLowerCase().indexOf(qLower) !== -1;
        if (nameMatches || descMatches || catMatches) {
          matched.push(p);
        }
      }
    }

    var results = matched.slice(0, limit);
    var prefix = getDepthPrefix();
    var html = '';

    if (results.length === 0) {
      html = '<div id="PredictiveSearchResults-' + sectionId + '">' +
        '<div class="search__results-section flex flex-col gap-3 text-center py-6">' +
        '<p class="text-color-light text-small">No results found for "' + escapeHtml(searchTerm) + '"</p>' +
        '</div>' +
        '</div>';
    } else {
      var rows = '';
      for (var j = 0; j < results.length; j++) {
        var p = results[j];
        var priceStr = '$' + p.price.toFixed(2);
        var imgUrl = p.mainImage ? (prefix + p.mainImage) : '';
        var href = prefix + folderSeparator + p.slug + '/index.html';
        
        rows += '<li class="search__result-item flex w-full">' +
          '<a class="flex items-center gap-4 w-full reversed-link" href="' + href + '">' +
          '<div class="media media--square shrink-0" style="width: 50px; height: 50px; --ratio: 1.0; border-radius: var(--media-border-radius, 8px); overflow: hidden; position: relative;">' +
          (imgUrl ? '<img class="media__image" src="' + imgUrl + '" alt="' + escapeHtml(p.name) + '" width="50" height="50" loading="lazy" style="object-fit: cover; width: 100%; height: 100%;">' : '') +
          '</div>' +
          '<div class="flex flex-col flex-grow text-left justify-center">' +
          '<span class="reversed-link__text text-small font-bold" style="font-weight: 600; font-size: 1.4rem; line-height: 1.2;">' + escapeHtml(p.name) + '</span>' +
          '<span class="text-small text-color-light font-medium" style="font-size: 1.2rem; opacity: 0.8; margin-top: 2px;">' + priceStr + '</span>' +
          '</div>' +
          '</a>' +
          '</li>';
      }

      html = '<div id="PredictiveSearchResults-' + sectionId + '">' +
        '<div class="search__results-section flex flex-col gap-3 w-full">' +
        '<h3 class="search__results-heading h6 text-capitalize">Products</h3>' +
        '<ul class="search__result-list--vertical list-unstyled flex flex-col gap-3">' +
        rows +
        '</ul>' +
        '<div class="border-top pt-3 flex justify-center">' +
        '<a href="' + prefix + 'search/index.html?q=' + encodeURIComponent(searchTerm) + '" class="btn btn--secondary btn--sm w-full text-center" style="font-size:1.2rem; padding: 0.6rem 1rem;">' +
        'View all results for "' + escapeHtml(searchTerm) + '"' +
        '</a>' +
        '</div>' +
        '</div>' +
        '</div>';
    }

    return new Response(html, {
      status: 200,
      headers: { 'Content-Type': 'text/html' }
    });
  }

  function handleUrlSearchQuery() {
    var params = new URLSearchParams(window.location.search);
    var query = params.get('q');
    if (!query) return;

    console.log('[Search] Found q parameter in URL:', query);

    // Try to open the search drawer dialog
    var searchDrawerDialog = document.getElementById('search-drawer-dialog');
    if (searchDrawerDialog) {
      try {
        if (!searchDrawerDialog.open) {
          searchDrawerDialog.showModal();
          searchDrawerDialog.setAttribute('open', '');
          document.documentElement.setAttribute('scroll-lock', '');
          document.documentElement.classList.add('scroll-locked');
        }
      } catch(e) {
        console.warn('[Search] Failed to open search drawer dialog:', e);
      }
    }

    // Find and prefill the inputs
    setTimeout(function() {
      var inputs = document.querySelectorAll('predictive-search input[name="q"]');
      for (var i = 0; i < inputs.length; i++) {
        var input = inputs[i];
        input.value = query;
        input.focus();
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }, 300);
  }

  // ---- Interceptor ----
  window.fetch = async function(resource, options) {
    // Wait for product cache to load if not already loaded
    var productCache = window.__rawjoyProductCache;
    if (!productCache) {
      productCache = await productCachePromise;
    }

    var url = typeof resource === 'string' ? resource : (resource && resource.url ? resource.url : '');

    var pathname = '';
    try {
      var absoluteUrl = url.indexOf('http') === 0 || url.indexOf('//') === 0 ? url : window.location.origin + (url.indexOf('/') === 0 ? '' : '/') + url;
      pathname = new URL(absoluteUrl).pathname;
    } catch (e) {
      pathname = url;
    }

    var isCart = pathname.indexOf('/cart/add') !== -1 || 
                pathname.indexOf('/cart/change') !== -1 ||
                pathname.indexOf('/cart/update') !== -1 || 
                pathname.indexOf('/cart/clear') !== -1 ||
                pathname === '/cart' || 
                pathname === '/cart/' ||
                pathname === '/cart.js';

    var isPredictiveSearch = pathname.indexOf('/search/suggest') !== -1;

    if (!isCart && !isPredictiveSearch) {
      return originalFetch.apply(this, arguments);
    }

    if (isPredictiveSearch) {
      return handlePredictiveSearch(url);
    }

    console.log('[Cart] Intercepted:', url);

    // Parse body
    var bodyData = {};
    if (options && options.body) {
      if (options.body instanceof FormData) {
        var entries = options.body.entries();
        var entry;
        while (!(entry = entries.next()).done) {
          bodyData[entry.value[0]] = entry.value[1];
        }
      } else if (typeof options.body === 'string') {
        try { bodyData = JSON.parse(options.body); } catch(e) {
          var params = new URLSearchParams(options.body);
          params.forEach(function(value, key) { bodyData[key] = value; });
        }
      }
    }

    console.log('[Cart] Body:', JSON.stringify(bodyData).substring(0, 200));

    // ADD TO CART
    if (url.indexOf('/cart/add') !== -1) {
      var itemsToAdd = [];
      if (Array.isArray(bodyData.items)) {
        for (var k = 0; k < bodyData.items.length; k++) {
          itemsToAdd.push({
            id: bodyData.items[k].id || bodyData.items[k].variant_id,
            quantity: parseInt(bodyData.items[k].quantity || 1, 10)
          });
        }
      } else {
        var idx = 0;
        while (true) {
          var itemIdKey = 'items[' + idx + '][id]';
          var itemQtyKey = 'items[' + idx + '][quantity]';
          if (bodyData[itemIdKey] !== undefined) {
            itemsToAdd.push({
              id: bodyData[itemIdKey],
              quantity: parseInt(bodyData[itemQtyKey] || 1, 10)
            });
            idx++;
          } else {
            break;
          }
        }
      }

      if (itemsToAdd.length === 0 && bodyData.id !== undefined) {
        itemsToAdd.push({
          id: bodyData.id,
          quantity: parseInt(bodyData.quantity || 1, 10)
        });
      }

      for (var j = 0; j < itemsToAdd.length; j++) {
        var itemToAdd = itemsToAdd[j];
        var id = itemToAdd.id;
        var qty = itemToAdd.quantity;
        var product = extractProduct(id);

        if (product) {
          if (isDummyBundleProduct(product)) {
            console.log('[Cart] Skipping dummy bundle product addition:', product.name);
            continue;
          }
          if (window.DB && window.DB.cart) {
            await window.DB.cart.add(product, qty, product.variant);
            console.log('[Cart] Added via DB Bridge:', product.name, 'x' + qty);
          } else {
            var cart = getCart();
            var existing = -1;
            for (var i = 0; i < cart.items.length; i++) {
              if (cart.items[i].productId === product.id && cart.items[i].variant === product.variant) {
                existing = i;
                break;
              }
            }
            if (existing >= 0) {
              cart.items[existing].quantity += qty;
            } else {
              cart.items.push({
                productId: product.id,
                name: product.name,
                price: product.price,
                quantity: qty,
                image: product.image || '',
                variant: product.variant,
                slug: product.slug
              });
            }
            saveCart(cart);
            console.log('[Cart] Added via LocalStorage fallback:', product.name, 'x' + qty);
          }
        } else {
          // Check if fallback ID maps to a dummy product
          var isDummy = false;
          var cacheList = window.__rawjoyProductCache || [];
          for (var i = 0; i < cacheList.length; i++) {
            if (cacheList[i].slug === id || cacheList[i].id === id) {
              if (isDummyBundleProduct(cacheList[i])) {
                isDummy = true;
              }
              break;
            }
          }
          if (isDummy) {
            console.log('[Cart] Skipping dummy bundle fallback product:', id);
            continue;
          }

          console.warn('[Cart] Fallback: creating placeholder for ID:', id);
          if (window.DB && window.DB.cart) {
            var fallbackProduct = {
              id: String(id),
              name: 'Product ' + String(id).slice(-4),
              slug: String(id),
              price: 0,
              mainImage: '',
              variants: []
            };
            await window.DB.cart.add(fallbackProduct, qty, null);
          } else {
            var cart2 = getCart();
            cart2.items.push({
              productId: String(id),
              name: 'Product ' + String(id).slice(-4),
              price: 0,
              quantity: qty,
              image: '',
              variant: null,
              slug: String(id)
            });
            saveCart(cart2);
          }
        }
      }
    }
    // CHANGE / UPDATE
    else if (url.indexOf('/cart/change') !== -1 || url.indexOf('/cart/update') !== -1) {
      var line = parseInt(bodyData.line, 10);
      var quantity = parseInt(bodyData.quantity, 10);
      
      if (window.DB && window.DB.cart) {
        var currentCart = await window.DB.cart.get();
        if (line && currentCart.items[line - 1]) {
          var targetItem = currentCart.items[line - 1];
          await window.DB.cart.update(targetItem.productId, quantity, targetItem.variant);
          console.log('[Cart] Updated via DB Bridge:', targetItem.name, 'qty:', quantity);
        }
      } else {
        var cart3 = getCart();
        if (line && cart3.items[line - 1]) {
          if (quantity <= 0) {
            cart3.items.splice(line - 1, 1);
          } else {
            cart3.items[line - 1].quantity = quantity;
          }
          saveCart(cart3);
          console.log('[Cart] Updated via LocalStorage fallback line:', line, 'qty:', quantity);
        }
      }
    }
    // CLEAR
    else if (url.indexOf('/cart/clear') !== -1) {
      if (window.DB && window.DB.cart) {
        await window.DB.cart.clear();
        console.log('[Cart] Cleared via DB Bridge');
      } else {
        saveCart({ items: [] });
        console.log('[Cart] Cleared via LocalStorage fallback');
      }
    }

    // Build response
    var updatedCart = (window.DB && window.DB.cart) ? await window.DB.cart.get() : getCart();
    var totalItems = updatedCart.items.reduce(function(sum, item) { return sum + item.quantity; }, 0);

    // Requested sections
    var requestedSections = [];
    if (bodyData.sections) {
      requestedSections = typeof bodyData.sections === 'string' ? bodyData.sections.split(',') : [bodyData.sections];
    }
    if (requestedSections.length === 0) {
      var cc = document.querySelector('cart-items-component');
      if (cc && cc.dataset && cc.dataset.sectionId) {
        requestedSections.push(cc.dataset.sectionId);
      } else {
        requestedSections.push('cart-drawer');
      }
    }

    var sections = {};
    for (var s = 0; s < requestedSections.length; s++) {
      sections[requestedSections[s]] = buildSectionsHTML(updatedCart, requestedSections[s]);
    }

    var mockResponse = {
      items: updatedCart.items.map(function(item) {
        return {
          id: item.productId,
          variant_id: item.productId,
          title: item.name,
          quantity: item.quantity,
          price: Math.round((item.price || 0) * 100),
          final_price: Math.round((item.price || 0) * 100),
          final_line_price: Math.round((item.price || 0) * (item.quantity || 1) * 100),
          url: (isFlattened ? '/products_' : '/products/') + item.slug + (isFlattened ? '/index.html' : '/'),
          image: item.image,
          featured_image: { url: item.image },
          variant_title: item.variant || null
        };
      }),
      item_count: totalItems,
      total_price: Math.round(updatedCart.total * 100),
      sections: sections
    };

    console.log('[Cart] Response: ' + totalItems + ' items');
    updateCartBadges(totalItems);
    
    // Only update and inject cart HTML if the request did not request sections
    // or if the cart items component is not present in the DOM.
    // This prevents destroying active DOM elements and event listeners during Ajax cycles.
    var cartItemsComp = document.querySelector('cart-items-component');
    if (!bodyData.sections || !cartItemsComp) {
      updateAndInjectCart();
    }

    // Auto-open drawer fallback for cart additions
    if (url.indexOf('/cart/add') !== -1) {
      setTimeout(function() {
        var cartDrawer = document.getElementById('CartDrawer');
        var dialog = document.getElementById('cart-drawer-dialog');
        
        if (cartDrawer && typeof cartDrawer.open === 'function') {
          try {
            cartDrawer.open();
            return;
          } catch(e) {}
        }
        
        if (dialog && !dialog.open) {
          console.log('[Cart Interceptor] Auto-opening cart drawer...');
          try {
            dialog.showModal();
            dialog.setAttribute('open', '');
            document.documentElement.setAttribute('scroll-lock', '');
            document.documentElement.classList.add('scroll-locked');
            
            var closeBtn = dialog.querySelector('.cart-drawer__close, .dialog__close');
            if (closeBtn) {
              closeBtn.addEventListener('click', function() {
                dialog.close();
                dialog.removeAttribute('open');
                document.documentElement.removeAttribute('scroll-lock');
                document.documentElement.classList.remove('scroll-locked');
              }, { once: true });
            }
          } catch(err) {
            console.error('[Cart] Auto-open fallback failed:', err);
          }
        }
      }, 300);
    }

    return new Response(JSON.stringify(mockResponse), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
  };

  // Also intercept /cart.js GET requests
  var origXHR = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function(method, url) {
    if (url && url.indexOf('/cart.js') !== -1) {
      this.__isCartRequest = true;
    }
    return origXHR.apply(this, arguments);
  };

  console.log('[Cart] Interceptor installed ✓');

  // ---- Fallback Cart Drawer Opener ----
  // The theme uses on:click="#CartDrawer/open" which relies on Component instanceof check.
  // If cart-drawer.js fails to load as a module (e.g., in file:// or WebView environments),
  // the cart-drawer-component custom element is never registered, so the on:click handler
  // silently returns. This fallback directly opens the dialog.
  function setupCartDrawerFallback() {
    // Global close handler for dialog (any click on close button inside the dialog)
    document.addEventListener('click', function(evt) {
      var closeBtn = evt.target.closest('#cart-drawer-dialog .cart-drawer__close, #cart-drawer-dialog .dialog__close');
      if (closeBtn) {
        var dialog = document.getElementById('cart-drawer-dialog');
        if (dialog && dialog.open) {
          dialog.close();
          dialog.removeAttribute('open');
          document.documentElement.removeAttribute('scroll-lock');
          document.documentElement.classList.remove('scroll-locked');
        }
      }
      
      // Backdrop click handler
      var dialog = evt.target.closest('#cart-drawer-dialog');
      if (dialog && evt.target === dialog && dialog.open) {
        var rect = dialog.getBoundingClientRect();
        var isInDialog = (evt.clientX >= rect.left && evt.clientX <= rect.right &&
                         evt.clientY >= rect.top && evt.clientY <= rect.bottom);
        if (!isInDialog) {
          dialog.close();
          dialog.removeAttribute('open');
          document.documentElement.removeAttribute('scroll-lock');
          document.documentElement.classList.remove('scroll-locked');
        }
      }
    });

    // Global keydown escape handler for dialog
    document.addEventListener('keydown', function(evt) {
      if (evt.key === 'Escape') {
        var dialog = document.getElementById('cart-drawer-dialog');
        if (dialog && dialog.open) {
          evt.preventDefault();
          dialog.close();
          dialog.removeAttribute('open');
          document.documentElement.removeAttribute('scroll-lock');
          document.documentElement.classList.remove('scroll-locked');
        }
      }
    });

    // 1. Global event delegation click interceptor (capture phase)
    document.addEventListener('click', function(e) {
      var target = e.target.closest('#cart-icon-bubble, a[on\\:click*="CartDrawer/open"], .cart-drawer-button, .header__icon--cart, a[aria-controls="cart-drawer-dialog"], a[href*="/cart"]');
      if (target) {
        // Exclude footer buttons or direct navigation links (like View Cart or Check Out)
        var href = target.getAttribute('href') || '';
        if (target.closest('.premium-cart-footer') || 
            target.closest('.cart-drawer__footer') || 
            target.classList.contains('footer-btn') || 
            href.indexOf('cart/index.html') !== -1 || 
            href.indexOf('checkout') !== -1) {
          console.log('[Cart] Bypassing interceptor for navigation link:', href);
          return;
        }

        console.log('[Cart] Global event delegation matched click on:', target);
        
        // Ensure cart HTML is updated in DOM before opening
        updateAndInjectCart();
        
        var cartDrawer = document.getElementById('CartDrawer');
        var dialog = document.getElementById('cart-drawer-dialog');
        
        // Let the custom element handle it first if it is defined and works
        if (cartDrawer && typeof cartDrawer.open === 'function') {
          try {
            e.preventDefault();
            e.stopPropagation();
            cartDrawer.open(e);
            console.log('[Cart] Opened via custom element open() delegation');
            return;
          } catch (err) {
            console.warn('[Cart] Custom element open() delegation failed:', err);
          }
        }
        
        // Manual dialog fallback opener
        if (dialog) {
          e.preventDefault();
          e.stopPropagation();
          try {
            if (!dialog.open) {
              dialog.showModal();
              dialog.setAttribute('open', '');
              document.documentElement.setAttribute('scroll-lock', '');
              document.documentElement.classList.add('scroll-locked');
              console.log('[Cart] Opened via manual showModal() delegation');
            }
          } catch (err) {
            console.error('[Cart] Manual showModal() delegation failed:', err);
          }
        }
      }
    }, true); // Use capture phase

    console.log('[Cart] Global Click Delegation Fallback opener installed ✓');
  }

  // Listen for cart update events
  document.addEventListener('cart:update', function() {
    updateAndInjectCart();
  });
  document.addEventListener('cart:updated', function() {
    updateAndInjectCart();
  });

  // Global search form interceptor
  document.addEventListener('submit', function(e) {
    var form = e.target.closest('form');
    if (!form) return;
    var action = form.getAttribute('action') || '';
    if (action === 'search' || action === '/search' || action.slice(-7) === '/search') {
      e.preventDefault();
      var qInput = form.querySelector('input[name="q"]');
      var query = qInput ? qInput.value.trim() : '';
      var prefix = getDepthPrefix();
      window.location.href = prefix + 'search/index.html?q=' + encodeURIComponent(query);
    }
  });

  function initCartState() {
    updateCartBadges();
    setupCartDrawerFallback();
    handleUrlSearchQuery();
    updateAndInjectCart();
    
    // Dynamically load auth-ui.js if not present
    if (!document.querySelector('script[src*="auth-ui.js"]')) {
      var authScript = document.createElement('script');
      authScript.type = 'module';
      authScript.src = prefix + 'js/auth-ui.js';
      document.head.appendChild(authScript);
    }

    if (window.DB && window.DB.cart) {
      window.DB.cart.get().then(function(c) {
        var count = c.items.reduce(function(sum, item) { return sum + item.quantity; }, 0);
        updateCartBadges(count);
        updateAndInjectCart();
      });
    }
  }

  // Update badges and inject cart on page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCartState);
  } else {
    initCartState();
  }

  window.addEventListener('pageshow', function(event) {
    console.log('[Cart Interceptor] pageshow triggered, persisted:', event.persisted);
    try {
      var dialog = document.getElementById('cart-drawer-dialog');
      if (dialog) {
        dialog.close();
        dialog.removeAttribute('open');
      }
      document.documentElement.removeAttribute('scroll-lock');
      document.documentElement.classList.remove('scroll-locked');
    } catch(e) {
      console.error('[Cart] Error resetting drawer on pageshow:', e);
    }
    initCartState();
  });

  // Global 404 Link & Form Interceptor for Subfolder Hosting
  (function() {
    function getSubfolderPrefix() {
      var pathname = window.location.pathname;
      var pathParts = pathname.split('/').filter(Boolean);
      var rootIndicators = ['products', 'collections', 'pages', 'blogs', 'policies', 'cart', 'search', 'contact', 'css', 'js', 'images', 'firebase', 'data', 'api'];
      
      var rootIndex = -1;
      for (var i = 0; i < pathParts.length; i++) {
        if (rootIndicators.indexOf(pathParts[i].toLowerCase()) !== -1) {
          rootIndex = i;
          break;
        }
      }
      
      if (rootIndex > 0) {
        return '/' + pathParts.slice(0, rootIndex).join('/');
      }
      
      var opIndex = pathname.toLowerCase().indexOf('/op/');
      if (opIndex !== -1) return pathname.substring(0, opIndex + 3);
      
      var rjIndex = pathname.toLowerCase().indexOf('/rawjoy/');
      if (rjIndex !== -1) return pathname.substring(0, rjIndex + 8);
      
      return '';
    }

    var subfolder = getSubfolderPrefix();
    if (subfolder) {
      console.log('[Routing Interceptor] Active subfolder base:', subfolder);
      
      document.addEventListener('click', function(e) {
        var anchor = e.target.closest('a');
        if (!anchor) return;
        
        var href = anchor.getAttribute('href');
        if (!href) return;
        
        if (href.indexOf('http') === 0 || href.indexOf('//') === 0 || href.indexOf('#') === 0 || href.indexOf('javascript:') === 0 || href.indexOf('mailto:') === 0 || href.indexOf('tel:') === 0) {
          return;
        }
        
        if (href.startsWith('/')) {
          var lowerHref = href.toLowerCase();
          var lowerSub = subfolder.toLowerCase();
          if (lowerHref === lowerSub || lowerHref.startsWith(lowerSub + '/')) {
            return;
          }
          
          var newHref = subfolder + href;
          if (!newHref.endsWith('/') && !newHref.includes('.') && !newHref.includes('?')) {
            newHref += '/';
          }
          
          e.preventDefault();
          window.location.href = newHref;
          console.log('[Routing Interceptor] Rewrote absolute URL:', href, '->', newHref);
        }
      }, true);

      document.addEventListener('submit', function(e) {
        var form = e.target.closest('form');
        if (!form) return;
        
        var action = form.getAttribute('action');
        if (!action) return;
        
        if (action.startsWith('/')) {
          var lowerAction = action.toLowerCase();
          var lowerSub = subfolder.toLowerCase();
          if (lowerAction === lowerSub || lowerAction.startsWith(lowerSub + '/')) {
            return;
          }
          
          var newAction = subfolder + action;
          form.setAttribute('action', newAction);
          console.log('[Routing Interceptor] Rewrote form action:', action, '->', newAction);
        }
      }, true);
    }
  })();
})();
