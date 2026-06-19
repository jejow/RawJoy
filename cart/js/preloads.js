
    (function() {
      var preconnectOrigins = ["https://cdn.shopify.com"];
      var scripts = ["/cdn/shopifycloud/checkout-web/assets/c1/polyfills.iRHCMwIP.js","/cdn/shopifycloud/checkout-web/assets/c1/app.CmztCFJR.js","/cdn/shopifycloud/checkout-web/assets/c1/esnext-vendor.CVnhuHdK.js","/cdn/shopifycloud/checkout-web/assets/c1/browser.3wkDjvAD.js","/cdn/shopifycloud/checkout-web/assets/c1/shared-is-shop-pay-active.DnBz7ku_.js","/cdn/shopifycloud/checkout-web/assets/c1/Theme-utilities.CseKBzVQ.js","/cdn/shopifycloud/checkout-web/assets/c1/images-payment-icon.C_9SDN8i.js","/cdn/shopifycloud/checkout-web/assets/c1/purchasing-company-isValidPurchasingCompanyBillingAddress.DdO7g5H-.js","/cdn/shopifycloud/checkout-web/assets/c1/utilities-object.Dg666yHS.js","/cdn/shopifycloud/checkout-web/assets/c1/shared-unactionable-errors.BsEcwdOw.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useShopPayCheckoutGqlVersion.elyHFp71.js","/cdn/shopifycloud/checkout-web/assets/c1/graphql-ShopPayCheckoutSessionQuery.QFRm5TjB.js","/cdn/shopifycloud/checkout-web/assets/c1/helpers-setAddressErrors.DVjEnRBO.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useUnauthenticatedErrorModal.Cj7k1tgU.js","/cdn/shopifycloud/checkout-web/assets/c1/images-flag-icon.C_eXYJRt.js","/cdn/shopifycloud/checkout-web/assets/c1/locale-en.Clu-esOI.js","/cdn/shopifycloud/checkout-web/assets/c1/page-OnePage.D3nuEOaq.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useWalletsTimeout.BXh6qZ8i.js","/cdn/shopifycloud/checkout-web/assets/c1/remember-me-hooks.C7TNauON.js","/cdn/shopifycloud/checkout-web/assets/c1/OffsitePaymentFailed.DTRIQ4LN.js","/cdn/shopifycloud/checkout-web/assets/c1/NoAddressLocationFullDetour.DPAKdPL5.js","/cdn/shopifycloud/checkout-web/assets/c1/SplitDeliveryMerchandiseContainer.CiDI3S9T.js","/cdn/shopifycloud/checkout-web/assets/c1/useShopPayButtonClassName.O8A9il_S.js","/cdn/shopifycloud/checkout-web/assets/c1/ChangeCompanyLocationLink.DGnFiYyA.js","/cdn/shopifycloud/checkout-web/assets/c1/WalletsSandbox-WalletSandbox.BnP9tuPp.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useForceShopPayUrl.DtA9ImgU.js","/cdn/shopifycloud/checkout-web/assets/c1/GooglePayButton-index.4NSTMkrQ.js","/cdn/shopifycloud/checkout-web/assets/c1/MarketsProDisclaimer.DysDEgCH.js","/cdn/shopifycloud/checkout-web/assets/c1/ShippingGroupsSummaryLine.BMQM8TNK.js","/cdn/shopifycloud/checkout-web/assets/c1/StackedMerchandisePreview.BxFijknm.js","/cdn/shopifycloud/checkout-web/assets/c1/AutocompleteField-hooks.ClZVL1R0.js","/cdn/shopifycloud/checkout-web/assets/c1/LocalizationExtensionField.BCk_EUQ_.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useShopPayPaymentRequiredMethod.vTgKlE20.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useUpdateCheckoutAddress.BWNos6S2.js","/cdn/shopifycloud/checkout-web/assets/c1/WalletLogo.BmQRexwI.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useGeneralPaymentErrorMessage.CbLDIg2D.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useShowShopPayOptin.Dk1mE3N2.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useShowCreateMoreAccountsGdprTreatment.CxJKQxwa.js","/cdn/shopifycloud/checkout-web/assets/c1/Section.PY72ue4z.js","/cdn/shopifycloud/checkout-web/assets/c1/MobileOrderSummary.53vWkqRz.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useOnePageFormSubmit.DoyI6Apy.js","/cdn/shopifycloud/checkout-web/assets/c1/PayPalOverCaptureInfoBanner.BRO5xbNQ.js","/cdn/shopifycloud/checkout-web/assets/c1/utilities-get-negotiation-input.53Vm1O4P.js","/cdn/shopifycloud/checkout-web/assets/c1/shop-cash-constants.DbbUQ7A2.js","/cdn/shopifycloud/checkout-web/assets/c1/redemption-constants.Cu2A-vp8.js","/cdn/shopifycloud/checkout-web/assets/c1/PaymentErrorBanner.Ck-xZ29v.js","/cdn/shopifycloud/checkout-web/assets/c1/StockProblems-StockProblemsLineItemList.CDeMil91.js","/cdn/shopifycloud/checkout-web/assets/c1/DutyOptions.cQiiwLP-.js","/cdn/shopifycloud/checkout-web/assets/c1/ShipmentBreakdown.DabfYXrQ.js","/cdn/shopifycloud/checkout-web/assets/c1/MerchandiseModal.u8O2ZtSc.js","/cdn/shopifycloud/checkout-web/assets/c1/extension-targets-shipping-options.BiBR4S5H.js","/cdn/shopifycloud/checkout-web/assets/c1/ShippingMethodSelector.BUp1SDrP.js","/cdn/shopifycloud/checkout-web/assets/c1/SubscriptionPriceBreakdown.vyYlhZnx.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useSubscribeMessenger.cNncUQ55.js"];
      var styles = ["/cdn/shopifycloud/checkout-web/assets/c1/assets/app.RHL-Fw7g.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/is-shop-pay-active.C-ppsiYq.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/utilities.F5mjvpnu.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/useUnauthenticatedErrorModal.CjEFV7zE.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/OnePage.BTKlz-bT.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/SplitDeliveryMerchandiseContainer.pVQgcb_P.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/LocalizationExtensionField.BFmd7_iA.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/MobileOrderSummary.CqVkJv9Z.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/useOnePageFormSubmit.BRUjVIS4.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/WalletLogo.CIy8uDiZ.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/ChangeCompanyLocationLink.uqpm88mq.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/Section.CU18S7Ap.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/useShopPayButtonClassName.BrcQzLuH.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/DutyOptions.LcqrKXE1.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/PayPalOverCaptureInfoBanner.CuS5ve3d.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/NoAddressLocationFullDetour.CpFaJIpx.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/WalletSandbox.CnR7qNLY.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/ShippingMethodSelector.B0hio2RO.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/SubscriptionPriceBreakdown.BSemv9tH.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/StackedMerchandisePreview.D6OuIVjc.css"];
      var fontPreconnectUrls = [];
      var fontPrefetchUrls = [];
      var imgPrefetchUrls = [];

      function preconnect(url, callback) {
        var link = document.createElement('link');
        link.rel = 'dns-prefetch preconnect';
        link.href = url;
        link.crossOrigin = '';
        link.onload = link.onerror = callback;
        document.head.appendChild(link);
      }

      function preconnectAssets() {
        var resources = preconnectOrigins.concat(fontPreconnectUrls);
        var index = 0;
        (function next() {
          var res = resources[index++];
          if (res) preconnect(res, next);
        })();
      }

      function prefetch(url, as, callback) {
        var link = document.createElement('link');
        if (link.relList.supports('prefetch')) {
          link.rel = 'prefetch';
          link.fetchPriority = 'low';
          link.as = as;
          if (as === 'font') link.type = 'font/woff2';
          link.href = url;
          link.crossOrigin = '';
          link.onload = link.onerror = callback;
          document.head.appendChild(link);
        } else {
          var xhr = new XMLHttpRequest();
          xhr.open('GET', url, true);
          xhr.onloadend = callback;
          xhr.send();
        }
      }

      function prefetchAssets() {
        var resources = [].concat(
          scripts.map(function(url) { return [url, 'script']; }),
          styles.map(function(url) { return [url, 'style']; }),
          fontPrefetchUrls.map(function(url) { return [url, 'font']; }),
          imgPrefetchUrls.map(function(url) { return [url, 'image']; })
        );
        var index = 0;
        function run() {
          var res = resources[index++];
          if (res) prefetch(res[0], res[1], next);
        }
        var next = (self.requestIdleCallback || setTimeout).bind(self, run);
        next();
      }

      function onLoaded() {
        try {
          if (parseFloat(navigator.connection.effectiveType) > 2 && !navigator.connection.saveData) {
            preconnectAssets();
            prefetchAssets();
          }
        } catch (e) {}
      }

      if (document.readyState === 'complete') {
        onLoaded();
      } else {
        addEventListener('load', onLoaded);
      }
    })();
  