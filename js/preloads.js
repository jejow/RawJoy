
    (function() {
      var preconnectOrigins = ["https://cdn.shopify.com"];
      var scripts = ["/cdn/shopifycloud/checkout-web/assets/c1/polyfills.iRHCMwIP.js","/cdn/shopifycloud/checkout-web/assets/c1/app.DsWxz3qG.js","/cdn/shopifycloud/checkout-web/assets/c1/esnext-vendor.DnwbTn14.js","/cdn/shopifycloud/checkout-web/assets/c1/browser.BRUQC0Sw.js","/cdn/shopifycloud/checkout-web/assets/c1/NotFound.CPiqCFWz.js","/cdn/shopifycloud/checkout-web/assets/c1/types-UnauthenticatedErrorModalPayload.C6QC5udQ.js","/cdn/shopifycloud/checkout-web/assets/c1/images-payment-icon.C_9SDN8i.js","/cdn/shopifycloud/checkout-web/assets/c1/utilities-shop-discount-offer.FtFbwcAV.js","/cdn/shopifycloud/checkout-web/assets/c1/utilities-alternativePaymentCurrency.NX4cINO8.js","/cdn/shopifycloud/checkout-web/assets/c1/shared-unactionable-errors.B9RfOnn6.js","/cdn/shopifycloud/checkout-web/assets/c1/helpers-installmentsNotSupportedForAddress.BOCZuYce.js","/cdn/shopifycloud/checkout-web/assets/c1/utils-getCommonShopPayExternalTelemetryAttributes.DpOp7xFP.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useShopPayCheckoutGqlVersion.Du6zqzvf.js","/cdn/shopifycloud/checkout-web/assets/c1/graphql-ShopPayCheckoutSessionQuery.DWBSRi0q.js","/cdn/shopifycloud/checkout-web/assets/c1/helpers-setAddressErrors.Cw2BbkNg.js","/cdn/shopifycloud/checkout-web/assets/c1/types-index.Xpeao3jF.js","/cdn/shopifycloud/checkout-web/assets/c1/images-flag-icon.C_eXYJRt.js","/cdn/shopifycloud/checkout-web/assets/c1/locale-en.CXVkHWV9.js","/cdn/shopifycloud/checkout-web/assets/c1/page-OnePage.BAzWyaTh.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useWalletsTimeout.D2F35q5p.js","/cdn/shopifycloud/checkout-web/assets/c1/remember-me-hooks.Cra7IqQ9.js","/cdn/shopifycloud/checkout-web/assets/c1/OffsitePaymentFailed.BLj9OY5b.js","/cdn/shopifycloud/checkout-web/assets/c1/NoAddressLocationFullDetour.DgVnTlyH.js","/cdn/shopifycloud/checkout-web/assets/c1/SplitDeliveryMerchandiseContainer.C4P8mWjK.js","/cdn/shopifycloud/checkout-web/assets/c1/useShopPayButtonClassName.DF4cBk6T.js","/cdn/shopifycloud/checkout-web/assets/c1/ChangeCompanyLocationLink.DkclaOsk.js","/cdn/shopifycloud/checkout-web/assets/c1/WalletsSandbox-WalletSandbox.B_fbfhwi.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useUnauthenticatedErrorModal.BdksG0ES.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useForceShopPayUrl.CHXW_6pc.js","/cdn/shopifycloud/checkout-web/assets/c1/GooglePayButton-index.Dy9QXdxn.js","/cdn/shopifycloud/checkout-web/assets/c1/MarketsProDisclaimer.DQ6XAU6O.js","/cdn/shopifycloud/checkout-web/assets/c1/ShippingGroupsSummaryLine.BwvatTs0.js","/cdn/shopifycloud/checkout-web/assets/c1/StackedMerchandisePreview.D3rvy-JV.js","/cdn/shopifycloud/checkout-web/assets/c1/AutocompleteField-hooks.Da0aKpth.js","/cdn/shopifycloud/checkout-web/assets/c1/LocalizationExtensionField.Cn6CvUbE.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useShopPayPaymentRequiredMethod.OeEf-DTb.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useUpdateCheckoutAddress.BSE_Yvzz.js","/cdn/shopifycloud/checkout-web/assets/c1/WalletLogo.DcUrazTe.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useGeneralPaymentErrorMessage.CjDc6ekl.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useShowShopPayOptin.uYP8pDiA.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useShowCreateMoreAccountsGdprTreatment.DalV4Y5D.js","/cdn/shopifycloud/checkout-web/assets/c1/Section.BGvjjfIP.js","/cdn/shopifycloud/checkout-web/assets/c1/MobileOrderSummary.C3O8z53y.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useOnePageFormSubmit.DT40MJH3.js","/cdn/shopifycloud/checkout-web/assets/c1/PayPalOverCaptureInfoBanner.trEO2G0W.js","/cdn/shopifycloud/checkout-web/assets/c1/utilities-get-negotiation-input.n6gvfNxC.js","/cdn/shopifycloud/checkout-web/assets/c1/shop-cash-constants.BMXRy04z.js","/cdn/shopifycloud/checkout-web/assets/c1/PaymentErrorBanner.DTvqQ_a_.js","/cdn/shopifycloud/checkout-web/assets/c1/StockProblems-StockProblemsLineItemList.Dwub6mbL.js","/cdn/shopifycloud/checkout-web/assets/c1/DutyOptions.A6jquSGN.js","/cdn/shopifycloud/checkout-web/assets/c1/ShipmentBreakdown.v9NHqKfe.js","/cdn/shopifycloud/checkout-web/assets/c1/MerchandiseModal.C5d9sL2-.js","/cdn/shopifycloud/checkout-web/assets/c1/extension-targets-shipping-options.yvfUvyrq.js","/cdn/shopifycloud/checkout-web/assets/c1/ShippingMethodSelector.D0n0uJW8.js","/cdn/shopifycloud/checkout-web/assets/c1/SubscriptionPriceBreakdown.BB5PJ87H.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useSubscribeMessenger.C4UX5QWO.js"];
      var styles = ["/cdn/shopifycloud/checkout-web/assets/c1/assets/app.kbFPPpOR.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/NotFound.Bz45BrAn.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/UnauthenticatedErrorModalPayload.D1hsMvAK.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/index.iFhC-FZy.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/OnePage.Db-FuZsA.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/SplitDeliveryMerchandiseContainer.CRDql5Io.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/LocalizationExtensionField.UsZTbb_4.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/MobileOrderSummary.CqVkJv9Z.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/useOnePageFormSubmit.BRUjVIS4.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/WalletLogo.CIy8uDiZ.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/ChangeCompanyLocationLink.uqpm88mq.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/Section.CU18S7Ap.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/useShopPayButtonClassName.BrcQzLuH.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/DutyOptions.LcqrKXE1.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/PayPalOverCaptureInfoBanner.CuS5ve3d.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/NoAddressLocationFullDetour.CpFaJIpx.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/WalletSandbox.CnR7qNLY.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/ShippingMethodSelector.B0hio2RO.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/SubscriptionPriceBreakdown.BSemv9tH.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/StackedMerchandisePreview.D6OuIVjc.css"];
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
  