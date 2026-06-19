import{Component}from"@theme/component";
import{DialogCloseEvent,DialogComponent}from"@theme/dialog";
import{ThemeEvents}from"@theme/events";
import{getIOSVersion}from"@theme/utilities";

function getSubfolderPrefix() {
  const pathname = window.location.pathname;
  const parts = pathname.split('/').filter(Boolean);
  const rootIndicators = ['products', 'collections', 'pages', 'blogs', 'policies', 'cart', 'search', 'contact', 'css', 'js', 'images', 'firebase', 'data', 'api'];
  const knownPages = ['index.html', 'index.php'];
  let subfolder = '';
  for (let i = 0; i < parts.length; i++) {
    const pLower = parts[i].toLowerCase();
    if (rootIndicators.indexOf(pLower) !== -1 || knownPages.indexOf(pLower) !== -1 || pLower.indexOf('.') !== -1) {
      if (i > 0) {
        subfolder = '/' + parts.slice(0, i).join('/') + '/';
      }
      break;
    }
  }
  if (!subfolder && parts.length > 0) {
    const firstPartLower = parts[0].toLowerCase();
    if (rootIndicators.indexOf(firstPartLower) === -1 && knownPages.indexOf(firstPartLower) === -1 && firstPartLower.indexOf('.') === -1) {
      subfolder = '/' + parts[0] + '/';
    }
  }
  return subfolder || '/';
}

function getBaseUrl(urlStr) {
  try {
    const subfolderPrefix = getSubfolderPrefix();
    let resolvedUrlStr = urlStr;
    if (subfolderPrefix !== '/') {
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
    const subfolderPrefix = getSubfolderPrefix();
    if (relUrl.startsWith('/') && !relUrl.startsWith('//')) {
      if (subfolderPrefix !== '/' && !relUrl.toLowerCase().startsWith(subfolderPrefix.toLowerCase())) {
        return subfolderPrefix + relUrl.substring(1);
      }
      return relUrl;
    }
    if (relUrl.startsWith('//')) {
      const afterProto = relUrl.substring(2);
      const host = window.location.host;
      if (subfolderPrefix !== '/' && afterProto.toLowerCase().startsWith(host.toLowerCase())) {
        const pathPart = afterProto.substring(host.length);
        if (!pathPart.toLowerCase().startsWith(subfolderPrefix.toLowerCase())) {
          return '//' + host + subfolderPrefix + pathPart.substring(1);
        }
      }
      return relUrl;
    }
    if (relUrl.startsWith('http:') || relUrl.startsWith('https:')) {
      if (subfolderPrefix !== '/' && relUrl.startsWith(window.location.origin)) {
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


export class QuickAddComponent extends Component{
  #abortController=null;
  #cachedContent=new Map;
  get productUrl(){return this.dataset?.productUrl}
  get productPageUrl(){
    const productLink=this.closest("product-card")?.getProductCardLink();
    if(!productLink?.href)return"";
    const url=new URL(productLink.href);
    if(url.searchParams.has("variant"))return url.toString();
    const selectedVariantId=this.#getSelectedVariantId();
    return selectedVariantId&&url.searchParams.set("variant",selectedVariantId),url.toString()
  }
  #getSelectedVariantId(){return this.closest("product-card")?.getSelectedVariantId()||null}
  connectedCallback(){
    super.connectedCallback(),
    this.quickAddButtonSpinner=this.querySelector(".quick-add__button-spinner"),
    this.quickAddButton=this.querySelector(".button-choose-options"),
    document.addEventListener(ThemeEvents.variantSelected,this.#updateQuickAddButtonState.bind(this))
  }
  disconnectedCallback(){
    super.disconnectedCallback(),
    document.removeEventListener(ThemeEvents.variantSelected,this.#updateQuickAddButtonState.bind(this)),
    this.#abortController?.abort()
  }
  #updateQuickAddButtonState(event){
    if(!(event.target instanceof HTMLElement)||this.dataset.quickAddMode==="view"||event.target.closest("product-card")!==this.closest("product-card"))return;
    const quickAddButton=this.dataset.productOptionsCount==="1"?"add":"choose";
    this.setAttribute("data-quick-add-button",quickAddButton)
  }
  #stayVisibleUntilDialogCloses(dialogComponent){
    this.toggleAttribute("stay-visible",!0),
    dialogComponent.addEventListener(DialogCloseEvent.eventName,()=>this.toggleAttribute("stay-visible",!1),{once:!0})
  }
  #openQuickAddModal=()=>{
    const dialogComponent=document.getElementById("quick-add-dialog");
    dialogComponent instanceof QuickAddDialog&&(this.#stayVisibleUntilDialogCloses(dialogComponent),dialogComponent.showDialog())
  };
  #closeQuickAddModal=()=>{
    const dialogComponent=document.getElementById("quick-add-dialog");
    dialogComponent instanceof QuickAddDialog&&dialogComponent.closeDialog()
  };
  handleClick=async event=>{
    event.preventDefault();
    const currentUrl=`${this.productPageUrl.split("?")[0]}?section_id=${this.quickAddDrawerId}&${this.productPageUrl.split("?")[1]}`;
    let quickAddContent=this.#cachedContent.get(currentUrl);
    if(!quickAddContent){
      this.addLoading();
      const html=await this.fetchProductPage(currentUrl);
      if(html){
        const quickAddContentElement=html.querySelector("[data-quick-add-content]");
        if(quickAddContentElement){
          rewriteElementPaths(quickAddContentElement, this.productPageUrl);
          quickAddContent=quickAddContentElement.cloneNode(!0);
          this.#cachedContent.set(currentUrl,quickAddContent);
        }
      }
      this.removeLoading()
    }
    if(quickAddContent){
      const freshContent=quickAddContent.cloneNode(!0);
      await this.updateQuickAddModal(freshContent)
    }
    this.#openQuickAddModal()
  };
  async fetchProductPage(productPageUrl){
    if(!productPageUrl)return null;
    this.#abortController?.abort(),this.#abortController=new AbortController;
    try{
      const response=await fetch(productPageUrl,{signal:this.#abortController.signal});
      if(!response.ok)throw new Error(`Failed to fetch product page: HTTP error ${response.status}`);
      const responseText=await response.text(),html=new DOMParser().parseFromString(responseText,"text/html");
      return document.dispatchEvent(new CustomEvent(ThemeEvents.quickViewLoaded,{detail:{productUrl:this.productUrl}})),html
    }catch(error){
      if(error.name==="AbortError")return null;
      throw error
    }finally{
      this.#abortController=null
    }
  }
  async updateQuickAddModal(quickAddContent){
    const quickAddDrawerContent=document.getElementById("quick-add-drawer-content");
    !quickAddContent||!quickAddDrawerContent||(quickAddDrawerContent.innerHTML=quickAddContent.innerHTML,this.#syncVariantSelection(quickAddContent))
  }
  #syncVariantSelection(modalContent){
    const selectedVariantId=this.#getSelectedVariantId();
    if(!selectedVariantId)return;
    const modalInputs=modalContent.querySelectorAll('input[type="radio"][data-variant-id]');
    for(const input of modalInputs)if(input instanceof HTMLInputElement&&input.dataset.variantId===selectedVariantId&&!input.checked){input.checked=!0,input.dispatchEvent(new Event("change",{bubbles:!0}));break}
  }
  addLoading(){this.quickAddButton?.classList.add("btn--loading"),this.quickAddButtonSpinner?.classList.remove("hidden")}
  removeLoading(){this.quickAddButton?.classList.remove("btn--loading"),this.quickAddButtonSpinner?.classList.add("hidden")}
  get quickAddDrawerId(){return document.getElementById("quick-add-drawer")?.dataset.sectionId}
}
customElements.get("quick-add-component")||customElements.define("quick-add-component",QuickAddComponent);

class QuickAddDialog extends DialogComponent{
  #abortController=new AbortController;
  #currentCartItemCount=null;
  connectedCallback(){
    super.connectedCallback(),
    this.#initializeCartCount(),
    this.addEventListener(ThemeEvents.cartUpdate,this.handleCartUpdate,{signal:this.#abortController.signal}),
    this.addEventListener(DialogCloseEvent.eventName,this.#handleDialogClose)
  }
  get productUrl(){return this.querySelector(".quick-add__content")?.dataset?.productUrl}
  showDialog(){super.showDialog(),document.dispatchEvent(new CustomEvent(ThemeEvents.quickViewOpened,{detail:{productUrl:this.productUrl}}))}
  disconnectedCallback(){super.disconnectedCallback(),this.#abortController.abort(),this.removeEventListener(DialogCloseEvent.eventName,this.#handleDialogClose)}
  #initializeCartCount(){
    const cartCountElement=document.querySelector('cart-count:not([data-context="drawer"])');
    if(cartCountElement?.refs?.cartBubbleCount){this.#currentCartItemCount=parseInt(cartCountElement.refs.cartBubbleCount.textContent??"0",10);return}
    const cartBubbleCount=document.querySelector(".cart-bubble__text-count");
    if(cartBubbleCount){this.#currentCartItemCount=parseInt(cartBubbleCount.textContent??"0",10);return}
    this.#currentCartItemCount=0
  }
  handleCartUpdate=event=>{
    if(event.detail.data?.didError)return;
    const itemCount=event.detail.data?.itemCount,isIncremental=event.detail.data?.isIncremental??!1;
    if(itemCount==null)return;
    let newCartItemCount;
    if(isIncremental){const currentCount2=this.#currentCartItemCount??0;newCartItemCount=Math.max(0,currentCount2+itemCount)}
    else newCartItemCount=Math.max(0,itemCount);
    const currentCount=this.#currentCartItemCount??0;
    newCartItemCount>currentCount&&this.closeDialog(),this.#currentCartItemCount=newCartItemCount
  };
  #updateProductTitleLink=event=>{
    const anchorElement=event.detail.data.html?.querySelector(".view-product-title a"),viewMoreDetailsLink=this.querySelector(".view-product-title a"),mobileProductTitle=this.querySelector(".product-header a");
    anchorElement&&(viewMoreDetailsLink&&(viewMoreDetailsLink.href=anchorElement.href),mobileProductTitle&&(mobileProductTitle.href=anchorElement.href))
  };
  #handleDialogClose=()=>{
    const iosVersion=getIOSVersion();
    !iosVersion||iosVersion.major>=17||iosVersion.major===16&&iosVersion.minor>=4||requestAnimationFrame(()=>{
      const grid=document.querySelector("#ResultsList [product-grid-view]");
      if(grid){
        const currentWidth=grid.getBoundingClientRect().width;
        grid.style.width=`${currentWidth-1}px`,requestAnimationFrame(()=>{grid.style.width=""})
      }
    })
  }
}
customElements.get("quick-add-dialog")||customElements.define("quick-add-dialog",QuickAddDialog);
//# sourceMappingURL=/cdn/shop/t/2/assets/quick-add.js.map?v=16553112235735488881776673949
