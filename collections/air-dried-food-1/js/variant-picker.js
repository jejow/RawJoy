import{Component}from"@theme/component";
import{ThemeEvents,VariantSelectedEvent,VariantUpdateEvent}from"@theme/events";
import{morph}from"@theme/morph";
import{requestIdleCallback,requestYieldCallback}from"@theme/utilities";

const globalVariantsCache=new Map,globalMediaCache=new Map;

function getBaseUrl(urlStr) {
  try {
    const pathname = window.location.pathname;
    const rawjoyIndex = pathname.toLowerCase().indexOf('/rawjoy');
    let subfolderPrefix = '';
    if (rawjoyIndex !== -1) {
      subfolderPrefix = pathname.substring(0, rawjoyIndex + 8); // "/RawJoy/" or "/rawjoy/"
    }

    let resolvedUrlStr = urlStr;
    if (subfolderPrefix) {
      if (urlStr.startsWith('/') && !urlStr.startsWith('//')) {
        if (!urlStr.toLowerCase().startsWith(subfolderPrefix.toLowerCase())) {
          resolvedUrlStr = subfolderPrefix + urlStr.substring(1);
        }
      } else if (urlStr.startsWith('//')) {
        const afterProto = urlStr.substring(2);
        const host = window.location.host;
        if (afterProto.toLowerCase().startsWith(host.toLowerCase())) {
          const pathPart = afterProto.substring(host.length);
          if (!pathPart.toLowerCase().startsWith(subfolderPrefix.toLowerCase())) {
            resolvedUrlStr = '//' + host + subfolderPrefix + pathPart.substring(1);
          }
        }
      } else if (urlStr.startsWith(window.location.origin)) {
        const pathPart = urlStr.substring(window.location.origin.length);
        if (!pathPart.toLowerCase().startsWith(subfolderPrefix.toLowerCase())) {
          resolvedUrlStr = window.location.origin + subfolderPrefix + pathPart.substring(1);
        }
      }
    }

    const url = new URL(resolvedUrlStr, window.location.href);
    let urlPathname = url.pathname;
    if (!urlPathname.endsWith('/') && !urlPathname.match(/\.[a-zA-Z0-9]+$/)) {
      urlPathname += '/';
    }
    url.pathname = urlPathname;
    url.search = '';
    url.hash = '';
    return url.toString();
  } catch (e) {
    console.error("Failed to parse URL:", urlStr, e);
    try {
      return new URL('./', window.location.href).toString();
    } catch(err) {
      return window.location.origin + "/";
    }
  }
}

function rewriteElementPaths(element, sourceUrl) {
  if (!element) return;
  const baseUrl = getBaseUrl(sourceUrl);
  
  const resolvePath = (relUrl) => {
    if (!relUrl || relUrl.startsWith("data:") || relUrl.startsWith("javascript:") || relUrl.startsWith("#")) {
      return relUrl;
    }
    const pathname = window.location.pathname;
    const rawjoyIndex = pathname.toLowerCase().indexOf('/rawjoy');
    let subfolderPrefix = '';
    if (rawjoyIndex !== -1) {
      subfolderPrefix = pathname.substring(0, rawjoyIndex + 8);
    }
    if (relUrl.startsWith('/') && !relUrl.startsWith('//')) {
      if (subfolderPrefix && !relUrl.toLowerCase().startsWith(subfolderPrefix.toLowerCase())) {
        return subfolderPrefix + relUrl.substring(1);
      }
      return relUrl;
    }
    if (relUrl.startsWith('//')) {
      const afterProto = relUrl.substring(2);
      const host = window.location.host;
      if (subfolderPrefix && afterProto.toLowerCase().startsWith(host.toLowerCase())) {
        const pathPart = afterProto.substring(host.length);
        if (!pathPart.toLowerCase().startsWith(subfolderPrefix.toLowerCase())) {
          return '//' + host + subfolderPrefix + pathPart.substring(1);
        }
      }
      return relUrl;
    }
    if (relUrl.startsWith('http:') || relUrl.startsWith('https:')) {
      if (subfolderPrefix && relUrl.startsWith(window.location.origin)) {
        const pathPart = relUrl.substring(window.location.origin.length);
        if (!pathPart.toLowerCase().startsWith(subfolderPrefix.toLowerCase())) {
          return window.location.origin + subfolderPrefix + pathPart.substring(1);
        }
      }
      return relUrl;
    }
    try {
      return new URL(relUrl, baseUrl).toString();
    } catch (e) {
      return relUrl;
    }
  };

  element.querySelectorAll("img, source, video").forEach(el => {
    if (el.hasAttribute("src")) {
      el.setAttribute("src", resolvePath(el.getAttribute("src")));
    }
    if (el.hasAttribute("srcset")) {
      const srcset = el.getAttribute("srcset");
      if (srcset) {
        try {
          const parts = srcset.split(",").map(part => {
            const trimmed = part.trim();
            if (!trimmed) return "";
            const match = trimmed.match(/^(\S+)(.*)$/);
            if (match) {
              return resolvePath(match[1]) + match[2];
            }
            return trimmed;
          });
          el.setAttribute("srcset", parts.filter(Boolean).join(", "));
        } catch (e) {}
      }
    }
  });

  element.querySelectorAll("a").forEach(el => {
    if (el.hasAttribute("href")) {
      el.setAttribute("href", resolvePath(el.getAttribute("href")));
    }
  });

  element.querySelectorAll("form").forEach(el => {
    if (el.hasAttribute("action")) {
      el.setAttribute("action", resolvePath(el.getAttribute("action")));
    }
  });

  element.querySelectorAll("[data-product-url]").forEach(el => {
    el.setAttribute("data-product-url", resolvePath(el.getAttribute("data-product-url")));
  });
  if (element.hasAttribute("data-product-url")) {
    element.setAttribute("data-product-url", resolvePath(element.getAttribute("data-product-url")));
  }
}

export default class VariantPicker extends Component{
  #pendingRequestUrl;
  #abortController;
  #lastProductId;
  connectedCallback(){
    super.connectedCallback(),
    this.#lastProductId=this.dataset.productId,
    this.#loadVariantsCache(),
    this.addEventListener("change",this.variantChanged.bind(this))
  }
  disconnectedCallback(){
    super.disconnectedCallback(),
    this.#abortController?.abort(),
    this.removeEventListener("change",this.variantChanged.bind(this))
  }
  updatedCallback(){
    super.updatedCallback?.();
    const currentProductId=this.dataset.productId;
    currentProductId!==this.#lastProductId&&(this.#lastProductId=currentProductId,this.#loadVariantsCache())
  }
  variantChanged(event){
    if(!(event.target instanceof HTMLElement))return;
    const selectedOption=event.target instanceof HTMLSelectElement?event.target.options[event.target.selectedIndex]:event.target;
    if(!selectedOption)return;
    this.updateSelectedOption(event.target),
    this.dispatchEvent(new VariantSelectedEvent({id:selectedOption.dataset.optionValueId??""}));
    const isOnProductPage=this.dataset.templateProductMatch==="true"&&!event.target.closest("product-card")&&!event.target.closest("quick-add-dialog"),
          currentUrl=this.dataset.productUrl?.split("?")[0],
          newUrl=selectedOption.dataset.connectedProductUrl,
          loadsNewProduct=isOnProductPage&&!!newUrl&&newUrl!==currentUrl,
          variantId=selectedOption.dataset.variantId,
          cachedVariant=this.#getCachedVariant();
    if(cachedVariant){
      this.#updateCriticalUI(cachedVariant,!0);
      const newProductUrl=selectedOption.dataset.connectedProductUrl,
            currentProductUrl=this.dataset.productUrl?.split("?")[0],
            hasProductChanged=newProductUrl&&currentProductUrl!==newProductUrl;
      this.selectedOptionId&&this.dispatchEvent(new VariantUpdateEvent(cachedVariant,this.selectedOptionId,{html:null,productId:this.dataset.productId??"",newProduct:hasProductChanged?{id:null,url:newProductUrl}:void 0,fromCache:!0})),
      requestIdleCallback(()=>{this.fetchUpdatedSection(this.buildRequestUrl(selectedOption),loadsNewProduct,!0)})
    }else if(variantId){
      const newProductUrl=selectedOption.dataset.connectedProductUrl,
            currentProductUrl=this.dataset.productUrl?.split("?")[0],
            hasProductChanged=newProductUrl&&currentProductUrl!==newProductUrl;
      this.#fetchVariantJson(variantId).then(variantData=>{
        variantData&&(this.#updateCriticalUI(variantData,!0),this.selectedOptionId&&this.dispatchEvent(new VariantUpdateEvent(variantData,this.selectedOptionId,{html:null,productId:this.dataset.productId??"",newProduct:hasProductChanged?{id:null,url:newProductUrl}:void 0,fromCache:!0})))
      }).catch(error=>{console.warn("Failed to fetch variant JSON:",error)}),
      requestIdleCallback(()=>{this.fetchUpdatedSection(this.buildRequestUrl(selectedOption),loadsNewProduct,!0)})
    }else this.fetchUpdatedSection(this.buildRequestUrl(selectedOption),loadsNewProduct,!1);
    const url=new URL(window.location.href);
    isOnProductPage&&(variantId?url.searchParams.set("variant",variantId):url.searchParams.delete("variant")),
    loadsNewProduct&&(url.pathname=newUrl),
    url.href!==window.location.href&&requestYieldCallback(()=>{history.replaceState({},"",url.toString())})
  }
  updateSelectedOption(target){
    if(typeof target=="string"){
      const targetElement=this.querySelector(`[data-option-value-id="${target}"]`);
      if(!targetElement)throw new Error("Target element not found");
      target=targetElement
    }
    if(target instanceof HTMLInputElement&&(target.checked=!0),target instanceof HTMLSelectElement){
      const newValue=target.value,
            newSelectedOption=Array.from(target.options).find(option=>option.value===newValue);
      if(!newSelectedOption)throw new Error("Option not found");
      for(const option of target.options)option.removeAttribute("selected");
      newSelectedOption.setAttribute("selected","selected")
    }
  }
  buildRequestUrl(selectedOption,source=null,sourceSelectedOptionsValues=[]){
    let productUrl=selectedOption.dataset.connectedProductUrl||this.#pendingRequestUrl||this.dataset.productUrl;
    this.#pendingRequestUrl=productUrl;
    const params=[];
    if(this.selectedOptionsValues.length&&!source?params.push(`option_values=${this.selectedOptionsValues.join(",")}`):source==="product-card"&&(this.selectedOptionsValues.length?params.push(`option_values=${sourceSelectedOptionsValues.join(",")}`):params.push(`option_values=${selectedOption.dataset.optionValueId}`)),this.closest("quick-add-dialog")||this.closest("swatches-variant-picker")){
      let sectionId=this.quickAddDrawerId;
      return this.closest("swatches-variant-picker")&&(sectionId="section-rendering-product-card"),
      productUrl?.includes("?")&&(productUrl=productUrl.split("?")[0]),
      `${productUrl}?section_id=${sectionId}&${params.join("&")}`
    }
    return`${productUrl}?${params.join("&")}`
  }
  fetchUpdatedSection(requestUrl,shouldMorphMain=!1,isBackgroundSync=!1){
    if(isBackgroundSync){console.log("[VariantPicker] Bypassing background sync fetch on static site");return}
    this.#abortController?.abort(),
    this.#abortController=new AbortController,
    fetch(requestUrl,{signal:this.#abortController.signal}).then(response=>response.text()).then(responseText=>{
      this.#pendingRequestUrl=void 0;
      const html=new DOMParser().parseFromString(responseText,"text/html");
      
      // Rewrite paths inside newly parsed html using requestUrl as reference
      rewriteElementPaths(html, requestUrl);
      
      const variantData=this.#extractVariantData(html);
      if(variantData?isBackgroundSync||this.#updateCriticalUI(variantData,!1):console.warn("No variant data extracted - dispatching without optimistic update"),shouldMorphMain)this.updateMain(html);
      else{
        const newProduct=this.updateVariantPicker(html);
        this.selectedOptionId&&this.dispatchEvent(new VariantUpdateEvent(variantData||null,this.selectedOptionId,{html,productId:this.dataset.productId??"",newProduct,fromCache:!1,isBackgroundSync}))
      }
    }).catch(error=>{error.name==="AbortError"?console.warn("Fetch aborted by user"):console.error(error)})
  }
  async#fetchVariantJson(variantId){
    if(!variantId)return null;
    try{
      const productUrl=this.dataset.productUrl||window.location.pathname,
            url=new URL(productUrl,window.location.origin);
      url.searchParams.set("sections","variant-data"),
      url.searchParams.set("variant",variantId),
      this.#abortController?.abort(),
      this.#abortController=new AbortController;
      const response=await fetch(url.toString(),{signal:this.#abortController.signal});
      if(!response.ok)return console.warn(`Variant JSON fetch failed: ${response.status}`),null;
      const htmlString=(await response.json())["variant-data"];
      if(!htmlString)return console.warn("No variant-data in response"),null;
      const tempDiv=document.createElement("div");
      tempDiv.innerHTML=htmlString;
      const sectionDiv=tempDiv.querySelector("#shopify-section-variant-data");
      return sectionDiv?.textContent?JSON.parse(sectionDiv.textContent):(console.warn("Could not extract JSON from section"),null)
    }catch(error){
      return error.name==="AbortError"||console.error("Error fetching variant JSON:",error),null
    }
  }
  #extractVariantData(html){
    const scriptTag=html.querySelector('variant-picker script[type="application/json"]');
    if(!scriptTag?.textContent)return console.warn("No variant data found in response"),null;
    try{return JSON.parse(scriptTag.textContent)}catch(e){return console.error("Failed to parse variant data:",e),null}
  }
  #updateCriticalUI(variantData,isFromCache=!1){
    this.#updatePriceOptimistic(variantData),
    isFromCache&&this.#updateMediaOptimistic(variantData),
    this.#updateButtonStateOptimistic(variantData),
    document.dispatchEvent(new CustomEvent(ThemeEvents.variantChanged,{detail:{variant:variantData}}))
  }
  #updatePriceOptimistic(variant){
    const priceComponent=(this.closest("product-card")||this.closest(".shopify-section, dialog"))?.querySelector("product-price");
    priceComponent&&priceComponent.dispatchEvent(new CustomEvent("price:update-optimistic",{detail:{variant},bubbles:!1}))
  }
  #updateMediaOptimistic(variant){
    if(!variant.featured_media)return;
    const mediaGallery=(this.closest("product-card")||this.closest(".shopify-section, dialog"))?.querySelector("media-gallery");
    mediaGallery&&mediaGallery.dispatchEvent(new CustomEvent("media:switch-optimistic",{detail:{variant},bubbles:!1}))
  }
  #updateButtonStateOptimistic(variant){
    const productForm=(this.closest("product-card")||this.closest(".shopify-section, dialog"))?.querySelector("product-form-component");
    if(!productForm)return;
    const addToCartButton=productForm.querySelector('[ref="addToCartButton"]');
    addToCartButton&&(addToCartButton.disabled=!variant.available)
  }
  updateVariantPicker(newHtml){
    if(!newHtml)return;
    let newProduct;
    const newVariantPickerSource=newHtml.querySelector(this.tagName.toLowerCase());
    if(!newVariantPickerSource)throw new Error("No new variant picker source found");
    if(newVariantPickerSource instanceof HTMLElement){
      const newProductId=newVariantPickerSource.dataset.productId,
            newProductUrl=newVariantPickerSource.dataset.productUrl;
      newProductId&&newProductUrl&&this.dataset.productId!==newProductId&&(newProduct={id:newProductId,url:newProductUrl}),
      this.dataset.productId=newProductId,
      this.dataset.productUrl=newProductUrl
    }
    return morph(this,newVariantPickerSource),newProduct
  }
  updateMain(newHtml){
    const main=document.querySelector("main"),
          newMain=newHtml.querySelector("main");
    if(!main||!newMain)throw new Error("No new main source found");
    morph(main,newMain)
  }
  get selectedOption(){
    const selectedOption=this.querySelector("select option[selected], .variant-option--fieldset input:checked");
    if(selectedOption instanceof HTMLInputElement||selectedOption instanceof HTMLOptionElement)return selectedOption
  }
  get selectedOptionId(){
    const{selectedOption}=this;
    if(!selectedOption)return;
    const{optionValueId}=selectedOption.dataset;
    if(!optionValueId)throw new Error("No option value ID found");
    return optionValueId
  }
  get selectedOptionsValues(){
    return Array.from(this.querySelectorAll("select option[selected], .variant-option--fieldset input:checked")).map(option=>{
      const{optionValueId}=option.dataset;
      if(!optionValueId)throw new Error("No option value ID found");
      return optionValueId
    })
  }
  get quickAddDrawerId(){return document.getElementById("quick-add-drawer")?.dataset.sectionId}
  #loadVariantsCache(){
    const cacheScript=this.querySelector("script[data-variants-cache]");
    if(!cacheScript?.textContent){console.warn("⚠️ No variants cache found - will fetch from server");return}
    const productId=this.dataset.productId;
    if(!productId){console.warn("No productId found - cannot cache variants");return}
    try{
      const data=JSON.parse(cacheScript.textContent);
      data.variants&&Array.isArray(data.variants)&&data.variants.forEach(variant=>{
        const key=this.#buildCacheKey(variant);
        globalVariantsCache.set(key,variant)
      }),
      data.media&&Array.isArray(data.media)&&data.media.forEach(media=>{
        const mediaKey=`${productId}|${media.id}`;
        globalMediaCache.set(mediaKey,media)
      })
    }catch(e){console.error("Failed to load variants cache:",e)}
  }
  #buildCacheKey(variant){
    const productId=this.dataset.productId;
    if(!productId)return console.warn("No productId for cache key"),"";
    const parts=[productId];
    return variant.option1&&parts.push(variant.option1),
    variant.option2&&parts.push(variant.option2),
    variant.option3&&parts.push(variant.option3),
    parts.join("|")
  }
  #getCachedVariant(){
    const productId=this.dataset.productId;
    if(!productId)return console.warn("No productId - cannot get cached variant"),null;
    const selectedOptions=Array.from(this.querySelectorAll("select option[selected], .variant-option--fieldset input:checked"));
    if(selectedOptions.length===0)return null;
    const optionValues=selectedOptions.map(el=>el.value).join("|"),
          key=`${productId}|${optionValues}`;
    return globalVariantsCache.get(key)||null
  }
}
customElements.get("variant-picker")||customElements.define("variant-picker",VariantPicker);
//# sourceMappingURL=/cdn/shop/t/2/assets/variant-picker.js.map?v=70267810711029563021776673948
