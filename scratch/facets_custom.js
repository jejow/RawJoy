import { sectionRenderer } from "@theme/section-renderer";
import { debounce, formatMoney } from "@theme/utilities";
import { FilterUpdateEvent, ThemeEvents } from "@theme/events";
import { Component } from "@theme/component";

const SEARCH_QUERY = "q";

const PRODUCT_METADATA = {
  "rawjoy-soft-bar": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Aura Interiors"
  },
  "salmon-stick": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Nest & Nook"
  },
  "cat-calming-formula": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Timeless Haven"
  },
  "cat-wellness-mix": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Timeless Haven"
  },
  "salmon-rice-formula": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Nest & Nook"
  },
  "mackerel-salmon-kibble": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Aura Interiors"
  },
  "chicken-pumpkin-pate": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Modern Oak"
  },
  "juicy-turkey-crunch": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Timeless Haven"
  },
  "salmon-carrot-pate": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Modern Oak"
  },
  "pet-meal-time-mix": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Timeless Haven"
  },
  "lamb-quinoa-blend": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Haven & Hearth"
  },
  "juicy-turkey-stick": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Nest & Nook"
  },
  "beef-spinach-stew": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Modern Oak"
  },
  "rawjoy-blue-energy-bar": {
    "variants": [],
    "vendor": "Nest & Nook"
  },
  "duck-soft-chews": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Timeless Haven"
  },
  "rawjoy-green-bar": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Aura Interiors"
  },
  "chicken-herb-stick": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Nest & Nook"
  },
  "mint-comfort-bowl-series": {
    "variants": [],
    "vendor": "Nest & Nook"
  },
  "fish-bone-treat": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Nest & Nook"
  },
  "chicken-bone-treat": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Nest & Nook"
  },
  "venison-peas-recipe": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Haven & Hearth"
  },
  "doggy-dental-mix": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Casa Curate"
  },
  "crunchy-bone-treat": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Aura Interiors"
  },
  "pastel-pet-bowl-series": {
    "variants": [],
    "vendor": "Nest & Nook"
  },
  "salmon-broccoli-crunch": {
    "variants": ["100gr", "150gr", "200gr"],
    "vendor": "Aura Interiors"
  }
};

class FacetsFormComponent extends Component {
  requiredRefs = ["facetsForm"];
  masterProducts = [];
  productCacheInitialized = false;
  usePagination = false;
  currentPage = 1;

  static #notifyCollectionRerendered = debounce(() => {
    document.dispatchEvent(new CustomEvent(ThemeEvents.collectionRerendered));
  }, 50);

  connectedCallback() {
    super.connectedCallback();
    
    // Detect initial page from URL path or query params
    const pathParts = window.location.pathname.split('/');
    const folderName = pathParts[pathParts.length - 2] || '';
    const match = folderName.match(/-(\d+)$/);
    if (match) {
      this.currentPage = parseInt(match[1], 10) + 1;
    } else {
      this.currentPage = 1;
    }
    const urlParams = new URLSearchParams(window.location.search);
    const pageParam = urlParams.get('page');
    if (pageParam) {
      this.currentPage = parseInt(pageParam, 10);
    }

    this.initProductCache();
  }

  async initProductCache() {
    if (this.productCacheInitialized) return;
    this.productCacheInitialized = true;

    const grid = document.querySelector('.product-grid');
    if (!grid) return;

    // Detect if pagination exists
    const initialPagination = document.querySelector('.pagination');
    this.usePagination = !!initialPagination;

    // Compile pagination page URLs in correct order
    const paginationList = document.querySelector('.pagination__list');
    const pageUrls = [];
    if (paginationList) {
      const items = Array.from(paginationList.querySelectorAll('li'));
      items.forEach(li => {
        const a = li.querySelector('a');
        const span = li.querySelector('span');
        if (a) {
          const isPrevNext = a.classList.contains('pagination__item--prev') || 
                             a.classList.contains('pagination__item--next') ||
                             a.innerText.trim().toLowerCase().includes('prev') ||
                             a.innerText.trim().toLowerCase().includes('next');
          if (!isPrevNext) {
            const href = a.getAttribute('href');
            if (href && href !== '#' && !href.startsWith('javascript:')) {
              pageUrls.push(new URL(href, window.location.href).href.split('?')[0]);
            }
          }
        } else if (span && span.classList.contains('pagination__item--current')) {
          pageUrls.push(window.location.href.split('?')[0]);
        }
      });
    }

    // Save initial products on current page
    const currentUrl = window.location.href.split('?')[0];
    const currentCards = Array.from(grid.querySelectorAll('li.product-grid__item'));
    const allPageCards = {};
    allPageCards[currentUrl] = currentCards;

    // Fetch sibling products in the background in order
    const siblingUrls = pageUrls.filter(url => url !== currentUrl);
    const fetchPromises = siblingUrls.map(async url => {
      try {
        const resp = await fetch(url);
        const text = await resp.text();
        const doc = new DOMParser().parseFromString(text, 'text/html');
        const cards = Array.from(doc.querySelectorAll('.product-grid li.product-grid__item'));
        return { url, cards };
      } catch (e) {
        console.error('Failed to fetch sibling products from', url, e);
        return { url, cards: [] };
      }
    });

    const results = await Promise.all(fetchPromises);
    results.forEach(res => {
      allPageCards[res.url] = res.cards;
    });

    // Compile master list in the correct page order
    this.masterProducts = [];
    if (pageUrls.length > 0) {
      pageUrls.forEach(url => {
        const cards = allPageCards[url] || [];
        cards.forEach(card => {
          const prodId = card.getAttribute('data-product-id');
          if (!this.masterProducts.some(c => c.getAttribute('data-product-id') === prodId)) {
            this.masterProducts.push(card);
          }
        });
      });
    } else {
      this.masterProducts = [...currentCards];
    }

    // Parse GTE/LTE initial limits from inputs
    const form = this.refs.facetsForm;
    if (form) {
      this.syncFormInputsWithURL();
    }

    this.updateCheckboxCounts();
    this.applyFiltersAndSorting();
  }

  updateCheckboxCounts() {
    const inputs = document.querySelectorAll('input[type="checkbox"][name^="filter."]');
    inputs.forEach(input => {
      let count = 0;
      const name = input.name;
      const value = input.value;

      if (name === 'filter.v.availability') {
        if (value === '1') {
          // In stock
          count = this.masterProducts.filter(card => {
            const isSoldOut = card.querySelector('.price--sold-out') || card.classList.contains('product-card--sold-out');
            return !isSoldOut;
          }).length;
        } else if (value === '0') {
          // Out of stock
          count = this.masterProducts.filter(card => {
            const isSoldOut = card.querySelector('.price--sold-out') || card.classList.contains('product-card--sold-out');
            return isSoldOut;
          }).length;
        }
      } else if (name === 'filter.v.t.shopify.accessory-size') {
        const sizeLabel = input.getAttribute('data-label') || value;
        count = this.masterProducts.filter(card => {
          const link = card.querySelector('a[href*="/products/"]');
          if (!link) return false;
          const href = link.getAttribute('href');
          const slugMatch = href.match(/\/products\/([^/?]+)/);
          const slug = slugMatch ? slugMatch[1] : '';
          const meta = PRODUCT_METADATA[slug];
          return meta && meta.variants && meta.variants.includes(sizeLabel);
        }).length;
      } else if (name === 'filter.p.vendor') {
        count = this.masterProducts.filter(card => {
          const link = card.querySelector('a[href*="/products/"]');
          if (!link) return false;
          const href = link.getAttribute('href');
          const slugMatch = href.match(/\/products\/([^/?]+)/);
          const slug = slugMatch ? slugMatch[1] : '';
          const meta = PRODUCT_METADATA[slug];
          return meta && meta.vendor === value;
        }).length;
      }

      // Find all matching inputs in the document (for both mobile/desktop facet forms)
      const matchingInputs = document.querySelectorAll(`input[name="${name}"][value="${value}"]`);
      matchingInputs.forEach(inp => {
        const label = inp.closest('label');
        if (label) {
          const span = label.querySelector('.checkbox__count, .facets__count');
          if (span) {
            span.textContent = count;
          }
        }
        if (count === 0) {
          inp.disabled = true;
          inp.closest('.facets__inputs-list-item')?.classList.add('facets__inputs-list-item--disabled');
        } else {
          inp.disabled = false;
          inp.closest('.facets__inputs-list-item')?.classList.remove('facets__inputs-list-item--disabled');
        }
      });
    });
  }


  createURLParameters(formData = new FormData(this.refs.facetsForm)) {
    let newParameters = new URLSearchParams(formData);
    newParameters.get("filter.v.price.gte") === "" && newParameters.delete("filter.v.price.gte");
    newParameters.get("filter.v.price.lte") === "" && newParameters.delete("filter.v.price.lte");
    newParameters.delete("page");
    const searchQuery = this.#getSearchQuery();
    return searchQuery && newParameters.set(SEARCH_QUERY, searchQuery), newParameters;
  }

  #getSearchQuery() {
    return new URL(window.location.href).searchParams.get(SEARCH_QUERY) ?? "";
  }

  get sectionId() {
    const id = this.getAttribute("section-id");
    if (!id) throw new Error("Section ID is required");
    return id;
  }

  #updateURLHash() {
    const url = new URL(window.location.href);
    const urlParameters = this.createURLParameters();
    url.search = "";
    for (const [param, value] of urlParameters.entries()) {
      url.searchParams.append(param, value);
    }
    history.pushState({ urlParameters: urlParameters.toString() }, "", url.toString());
  }

  updateFilters = () => {
    this.#updateURLHash();
    this.dispatchEvent(new FilterUpdateEvent(this.createURLParameters()));
    this.applyFiltersAndSorting();
  };

  async updateFiltersByURL(url) {
    history.pushState("", "", url);
    this.dispatchEvent(new FilterUpdateEvent(this.createURLParameters()));
    this.syncFormInputsWithURL();
    this.applyFiltersAndSorting();
    this.scrollToTop();
  }

  syncFormInputsWithURL() {
    const form = this.refs.facetsForm;
    if (!form) return;

    const urlParams = new URLSearchParams(window.location.search);

    // Checkboxes
    form.querySelectorAll('input[type="checkbox"]').forEach(input => {
      const name = input.name;
      const value = input.value;
      const values = urlParams.getAll(name);
      input.checked = values.includes(value);
    });

    // Price range inputs
    const gteInput = form.querySelector('#Price-GTE');
    if (gteInput) gteInput.value = urlParams.get('filter.v.price.gte') || '';

    const lteInput = form.querySelector('#Price-LTE');
    if (lteInput) lteInput.value = urlParams.get('filter.v.price.lte') || '';

    const gteInputDrawer = form.querySelector('#Price-GTE-in-drawer');
    if (gteInputDrawer) gteInputDrawer.value = urlParams.get('filter.v.price.gte') || '';

    const lteInputDrawer = form.querySelector('#Price-LTE-in-drawer');
    if (lteInputDrawer) lteInputDrawer.value = urlParams.get('filter.v.price.lte') || '';

    // Sorting select
    const sortSelect = document.querySelector('.sorting-filter__select');
    if (sortSelect) {
      sortSelect.value = urlParams.get('sort_by') || 'best-selling';
    }
  }

  applyFiltersAndSorting() {
    const form = this.refs.facetsForm;
    if (!form) return;

    const formData = new FormData(form);

    // Extract filters
    const availabilityChecked = formData.getAll('filter.v.availability');
    const minPriceVal = parseFloat((formData.get('filter.v.price.gte') || '').replace(',', '.'));
    const maxPriceVal = parseFloat((formData.get('filter.v.price.lte') || '').replace(',', '.'));

    const checkedSizeLabels = [];
    form.querySelectorAll('input[name="filter.v.t.shopify.accessory-size"]:checked').forEach(cb => {
      checkedSizeLabels.push(cb.getAttribute('data-label') || cb.value);
    });

    const brandsChecked = formData.getAll('filter.p.vendor');

    // Filter cards
    let filtered = [...this.masterProducts];

    filtered = filtered.filter(card => {
      const link = card.querySelector('a[href*="/products/"]');
      if (!link) return true;
      const href = link.getAttribute('href');
      const slugMatch = href.match(/\/products\/([^/?]+)/);
      const slug = slugMatch ? slugMatch[1] : '';

      const meta = PRODUCT_METADATA[slug] || { variants: [], vendor: "" };

      // Availability Filter
      if (availabilityChecked.length > 0 && availabilityChecked.length < 2) {
        const mode = availabilityChecked[0];
        const isSoldOut = card.querySelector('.price--sold-out') || card.classList.contains('product-card--sold-out');
        if (mode === "1" && isSoldOut) return false;
        if (mode === "0" && !isSoldOut) return false;
      }

      // Price Filter
      const priceTextEl = card.querySelector('.price--sale, .price__regular .price, .price');
      if (priceTextEl) {
        const priceText = priceTextEl.textContent || '';
        const priceMatch = priceText.match(/\$?([\d.,]+)/);
        if (priceMatch) {
          const price = parseFloat(priceMatch[1].replace(',', '.'));
          if (!isNaN(minPriceVal) && price < minPriceVal) return false;
          if (!isNaN(maxPriceVal) && price > maxPriceVal) return false;
        }
      }

      // Size Filter
      if (checkedSizeLabels.length > 0) {
        const matchesSize = meta.variants.some(v => checkedSizeLabels.includes(v));
        if (!matchesSize) return false;
      }

      // Brand Filter
      if (brandsChecked.length > 0) {
        if (!brandsChecked.includes(meta.vendor)) return false;
      }

      return true;
    });

    // Sorting
    const sortSelect = document.querySelector('.sorting-filter__select');
    const sortBy = sortSelect ? sortSelect.value : 'best-selling';

    if (sortBy === 'price-ascending') {
      filtered.sort((a, b) => this.getCardPrice(a) - this.getCardPrice(b));
    } else if (sortBy === 'price-descending') {
      filtered.sort((a, b) => this.getCardPrice(b) - this.getCardPrice(a));
    } else if (sortBy === 'title-ascending') {
      filtered.sort((a, b) => this.getCardTitle(a).localeCompare(this.getCardTitle(b)));
    } else if (sortBy === 'title-descending') {
      filtered.sort((a, b) => this.getCardTitle(b).localeCompare(this.getCardTitle(a)));
    } else {
      // Keep original order
      filtered.sort((a, b) => this.masterProducts.indexOf(a) - this.masterProducts.indexOf(b));
    }

    this.renderProducts(filtered);
  }

  getCardPrice(card) {
    const el = card.querySelector('.price-container .price--sale, .price-container .price, .price');
    if (el) {
      const m = el.textContent.match(/\$?([\d.,]+)/);
      if (m) return parseFloat(m[1].replace(',', '.'));
    }
    return 0;
  }

  getCardTitle(card) {
    const el = card.querySelector('.product-card__title .reversed-link__text, .product-card__title');
    return el ? el.textContent.trim() : '';
  }

  renderProducts(products) {
    const grid = document.querySelector('.product-grid');
    if (!grid) return;

    grid.innerHTML = '';

    const noResults = document.querySelector('.collection-empty') || document.querySelector('.facets-vertical__results-list-empty');

    if (products.length === 0) {
      if (noResults) noResults.style.display = 'block';
      this.updateProductCount(0);
      this.updatePagination(0, 1);
      FacetsFormComponent.#notifyCollectionRerendered();
      return;
    }

    if (noResults) noResults.style.display = 'none';
    this.updateProductCount(products.length);

    if (this.usePagination) {
      const pageSize = 12;
      const totalPages = Math.ceil(products.length / pageSize);
      const currentPage = Math.min(this.currentPage || 1, totalPages);
      this.currentPage = currentPage;

      const start = (currentPage - 1) * pageSize;
      const end = start + pageSize;
      const pageProducts = products.slice(start, end);

      for (const card of pageProducts) {
        grid.appendChild(card);
      }

      this.updatePagination(products.length, totalPages);
    } else {
      for (const card of products) {
        grid.appendChild(card);
      }
      const pag = document.querySelector('.pagination');
      if (pag) pag.style.display = 'none';
    }

    FacetsFormComponent.#notifyCollectionRerendered();
  }

  updateProductCount(count) {
    const elements = document.querySelectorAll('.products-count-wrapper span[title="Product count"], .products-count-wrapper span, [title="Product count"]');
    elements.forEach(el => {
      el.textContent = `${count} product${count !== 1 ? 's' : ''}`;
    });
  }

  updatePagination(totalCount, totalPages) {
    const pag = document.querySelector('.pagination');
    if (!pag) return;

    if (totalPages <= 1) {
      pag.style.display = 'none';
      return;
    }

    pag.style.display = '';
    const list = pag.querySelector('.pagination__list');
    if (!list) return;

    list.innerHTML = '';

    // Prev Button
    if (this.currentPage > 1) {
      const prevLi = document.createElement('li');
      prevLi.className = 'reversed-link';
      const prevA = document.createElement('a');
      prevA.className = 'pagination__item pagination__item--prev pagination__item-arrow motion-reduce';
      prevA.href = '#';
      prevA.innerHTML = `
        <span class="icon icon--caret-left icon--small">
          <svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
            <path d="M0 0H20V20H0V0z" fill="none"></path>
            <path d="M12.5 3.75L6.25 10L12.5 16.25" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
          </svg>
        </span>
        <span class="reversed-link__text">Prev</span>
      `;
      prevA.addEventListener('click', (e) => {
        e.preventDefault();
        this.currentPage--;
        this.applyFiltersAndSorting();
        this.scrollToTop();
      });
      prevLi.appendChild(prevA);
      list.appendChild(prevLi);
    }

    // Pages
    for (let p = 1; p <= totalPages; p++) {
      const li = document.createElement('li');
      const a = document.createElement('a');
      if (p === this.currentPage) {
        a.setAttribute('aria-current', 'page');
        a.setAttribute('aria-disabled', 'true');
        a.setAttribute('aria-label', `Page ${p}`);
        a.className = 'pagination__item pagination__item--current background-2';
        a.role = 'link';
        a.textContent = p;
      } else {
        a.setAttribute('aria-label', `Page ${p}`);
        a.className = 'pagination__item reversed-link';
        a.href = '#';
        a.innerHTML = `<span class="reversed-link__text">${p}</span>`;
        a.addEventListener('click', (e) => {
          e.preventDefault();
          this.currentPage = p;
          this.applyFiltersAndSorting();
          this.scrollToTop();
        });
      }
      li.appendChild(a);
      list.appendChild(li);
    }

    // Next Button
    if (this.currentPage < totalPages) {
      const nextLi = document.createElement('li');
      nextLi.className = 'reversed-link';
      const nextA = document.createElement('a');
      nextA.className = 'pagination__item pagination__item--next pagination__item-arrow motion-reduce';
      nextA.href = '#';
      nextA.innerHTML = `
        <span class="reversed-link__text">Next</span>
        <span class="icon icon--caret-right icon--small">
          <svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
            <path d="M0 0H20V20H0V0z" fill="none"></path>
            <path d="M7.5 3.75L13.75 10L7.5 16.25" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
          </svg>
        </span>
      `;
      nextA.addEventListener('click', (e) => {
        e.preventDefault();
        this.currentPage++;
        this.applyFiltersAndSorting();
        this.scrollToTop();
      });
      nextLi.appendChild(nextA);
      list.appendChild(nextLi);
    }
  }

  scrollToTop() {
    const targetElement = document.querySelector(".main-collection") || document.body;
    if (targetElement) {
      const headerHeight = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--header-height")) || 0;
      const targetRect = targetElement.getBoundingClientRect();
      const targetTop = window.scrollY + targetRect.top - headerHeight;
      window.scrollTo({ top: Math.max(0, targetTop), behavior: "smooth" });
    }
  }
}

customElements.get("facets-form-component") || customElements.define("facets-form-component", FacetsFormComponent);

class FacetInputsComponent extends Component {
  get sectionId() {
    const id = this.closest(".shopify-section")?.id;
    if (!id) throw new Error("FacetInputs component must be a child of a section");
    return id;
  }
  updateFilters() {
    const facetsForm = this.closest("facets-form-component");
    facetsForm instanceof FacetsFormComponent && facetsForm.updateFilters();
  }
  handleKeyDown(event) {
    if (!(event.target instanceof HTMLElement)) return;
    const closestInput = event.target.querySelector("input");
    closestInput instanceof HTMLInputElement && (event.key === "Enter" || event.key === " ") && (event.preventDefault(), closestInput.checked = !closestInput.checked, this.updateFilters());
  }
  prefetchPage = () => {};
  cancelPrefetchPage = () => {};
}

customElements.get("facet-inputs-component") || customElements.define("facet-inputs-component", FacetInputsComponent);

class PriceFacetComponent extends Component {
  connectedCallback() {
    super.connectedCallback();
    this.addEventListener("keydown", this.#onKeyDown);
    this.#initializeRangeInputs();
  }
  disconnectedCallback() {
    super.disconnectedCallback();
    this.removeEventListener("keydown", this.#onKeyDown);
    this.#cleanupRangeInputs();
  }
  #onKeyDown = event => {
    if (event.metaKey) return;
    const pattern = /[0-9]|\.|,|'| |Tab|Backspace|Enter|ArrowUp|ArrowDown|ArrowLeft|ArrowRight|Delete|Escape/;
    event.key.match(pattern) || event.preventDefault();
  };
  updatePriceFilterAndResults() {
    const { minInput, maxInput } = this.refs;
    this.#adjustToValidValues(minInput);
    this.#adjustToValidValues(maxInput);
    const facetsForm = this.closest("facets-form-component");
    facetsForm instanceof FacetsFormComponent && (facetsForm.updateFilters(), this.#setMinAndMaxValues());
  }
  #adjustToValidValues(input) {
    if (input.value.trim() === "") return;
    const value = Number(input.value);
    const min = Number(formatMoney(input.getAttribute("data-min") ?? ""));
    const max = Number(formatMoney(input.getAttribute("data-max") ?? ""));
    value < min && (input.value = min.toString());
    value > max && (input.value = max.toString());
  }
  #setMinAndMaxValues() {
    const { minInput, maxInput } = this.refs;
    maxInput.value && minInput.setAttribute("data-max", maxInput.value);
    minInput.value && maxInput.setAttribute("data-min", minInput.value);
    minInput.value === "" && maxInput.setAttribute("data-min", "0");
    maxInput.value === "" && minInput.setAttribute("data-max", minInput.getAttribute("data-max") ?? "");
  }
  #initializeRangeInputs() {
    const { rangeMin, rangeMax, minInput, maxInput } = this.refs;
    if (!rangeMin || !rangeMax) return;
    rangeMin.addEventListener("input", this.#onRangeMinInput);
    rangeMax.addEventListener("input", this.#onRangeMaxInput);
    rangeMin.addEventListener("change", this.#onRangeMinChange);
    rangeMax.addEventListener("change", this.#onRangeMaxChange);
    minInput.addEventListener("change", this.#onMinInputChange);
    maxInput.addEventListener("change", this.#onMaxInputChange);
    this.#updateRangeVisual();
  }
  #cleanupRangeInputs() {
    const { rangeMin, rangeMax, minInput, maxInput } = this.refs;
    rangeMin && (rangeMin.removeEventListener("input", this.#onRangeMinInput), rangeMin.removeEventListener("change", this.#onRangeMinChange));
    rangeMax && (rangeMax.removeEventListener("input", this.#onRangeMaxInput), rangeMax.removeEventListener("change", this.#onRangeMaxChange));
    minInput && minInput.removeEventListener("change", this.#onMinInputChange);
    maxInput && maxInput.removeEventListener("change", this.#onMaxInputChange);
  }
  #onRangeMinInput = event => {
    const { rangeMax, minInput } = this.refs;
    const value = parseInt(event.target.value);
    const maxValue = parseInt(rangeMax.value);
    value >= maxValue && (event.target.value = maxValue - 1);
    minInput.value = this.#centsToMoney(parseInt(event.target.value));
    this.#updateRangeVisual();
  };
  #onRangeMaxInput = event => {
    const { rangeMin, maxInput } = this.refs;
    const value = parseInt(event.target.value);
    const minValue = parseInt(rangeMin.value);
    value <= minValue && (event.target.value = minValue + 1);
    maxInput.value = this.#centsToMoney(parseInt(event.target.value));
    this.#updateRangeVisual();
  };
  #onRangeMinChange = () => {
    this.updatePriceFilterAndResults();
  };
  #onRangeMaxChange = () => {
    this.updatePriceFilterAndResults();
  };
  #centsToMoney(cents) {
    return (cents / 100).toLocaleString("de-DE", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }
  #moneyToCents(money) {
    const cleanNumber = formatMoney(String(money));
    return Math.round(parseFloat(cleanNumber) * 100);
  }
  #onMinInputChange = event => {
    const { rangeMin, maxInput } = this.refs;
    const valueInCents = this.#moneyToCents(event.target.value) || 0;
    const maxInCents = this.#moneyToCents(maxInput.value) || parseInt(rangeMin.max);
    const minRange = parseInt(rangeMin.min) || 0;
    const constrainedValue = Math.max(minRange, Math.min(valueInCents, maxInCents - 1));
    event.target.value = this.#centsToMoney(constrainedValue);
    rangeMin.value = constrainedValue;
    this.#updateRangeVisual();
  };
  #onMaxInputChange = event => {
    const { rangeMax, minInput } = this.refs;
    const valueInCents = this.#moneyToCents(event.target.value) || parseInt(rangeMax.max);
    const minInCents = this.#moneyToCents(minInput.value) || 0;
    const maxRange = parseInt(rangeMax.max);
    const constrainedValue = Math.min(maxRange, Math.max(valueInCents, minInCents + 1));
    event.target.value = this.#centsToMoney(constrainedValue);
    rangeMax.value = constrainedValue;
    this.#updateRangeVisual();
  };
  #updateRangeVisual() {
    const { rangeMin, rangeMax } = this.refs;
    if (!rangeMin || !rangeMax) return;
    const rangeInputs = this.querySelector(".price-facet__range-inputs");
    if (!rangeInputs) return;
    const minValue = parseInt(rangeMin.value);
    const maxValue = parseInt(rangeMax.value);
    const maxRange = parseInt(rangeMax.max);
    const minPercent = (minValue / maxRange) * 100;
    const maxPercent = (maxValue / maxRange) * 100;
    rangeInputs.style.setProperty("--range-min", `${minPercent}%`);
    rangeInputs.style.setProperty("--range-max", `${maxPercent}%`);
  }
}

customElements.get("price-facet-component") || customElements.define("price-facet-component", PriceFacetComponent);

class SortingFilterComponent extends Component {
  connectedCallback() {
    super.connectedCallback();
    const select = this.querySelector(".sorting-filter__select");
    const radioInputs = this.querySelectorAll(".sorting-filter__radio");
    select && select.addEventListener("change", this.updateFilterAndSorting);
    radioInputs.forEach(radio => {
      radio.addEventListener("change", this.updateFilterAndSorting);
    });
  }
  updateFilterAndSorting = event => {
    const facetsForm = this.closest("facets-form-component") || this.closest(".shopify-section")?.querySelector("facets-form-component");
    facetsForm instanceof FacetsFormComponent && facetsForm.updateFilters();
  };
}

customElements.get("sorting-filter-component") || customElements.define("sorting-filter-component", SortingFilterComponent);

class FacetRemoveComponent extends Component {
  connectedCallback() {
    super.connectedCallback();
    document.addEventListener(ThemeEvents.FilterUpdate, this.#handleFilterUpdate);
  }
  disconnectedCallback() {
    super.disconnectedCallback();
    document.removeEventListener(ThemeEvents.FilterUpdate, this.#handleFilterUpdate);
  }
  removeFilter({ form }, event) {
    if (event instanceof KeyboardEvent) {
      if (event.key !== "Enter" && event.key !== " ") return;
      event.preventDefault();
    }
    const url = this.dataset.url;
    if (!url) return;
    let facetsForm;
    form ? (facetsForm = document.getElementById(form)) : ((facetsForm = this.closest("facets-form-component")), facetsForm || (facetsForm = document.querySelector("facets-form-component")));
    facetsForm instanceof FacetsFormComponent && facetsForm.updateFiltersByURL(url);
  }
  #handleFilterUpdate = event => {
    const { clearButton } = this.refs;
    clearButton instanceof Element && clearButton.classList.toggle("active", event.shouldShowClearAll());
  };
}

customElements.get("facet-remove-component") || customElements.define("facet-remove-component", FacetRemoveComponent);
