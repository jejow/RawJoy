
    (function() {
      var preconnectOrigins = ["https://cdn.shopify.com"];
      var scripts = ["/cdn/shopifycloud/checkout-web/assets/c1/polyfills.iRHCMwIP.js","/cdn/shopifycloud/checkout-web/assets/c1/app.D8BW8pvr.js","/cdn/shopifycloud/checkout-web/assets/c1/esnext-vendor.Ca5G9khX.js","/cdn/shopifycloud/checkout-web/assets/c1/browser.yNvMKdOE.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useReplaceShopPayInHistory.w2wWjp5y.js","/cdn/shopifycloud/checkout-web/assets/c1/Theme-utilities.CD73Ex42.js","/cdn/shopifycloud/checkout-web/assets/c1/images-payment-icon.C_9SDN8i.js","/cdn/shopifycloud/checkout-web/assets/c1/utilities-object.CiYFcVBP.js","/cdn/shopifycloud/checkout-web/assets/c1/purchasing-company-isValidPurchasingCompanyBillingAddress.RTi2mYEY.js","/cdn/shopifycloud/checkout-web/assets/c1/utils-getCommonShopPayExternalTelemetryAttributes.ClAlRfGj.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useShopPayCheckoutGqlVersion.C3zDAmQX.js","/cdn/shopifycloud/checkout-web/assets/c1/FullScreenBackground.SLBVZd3X.js","/cdn/shopifycloud/checkout-web/assets/c1/graphql-ShopPayCheckoutSessionQuery.H7OXGE2y.js","/cdn/shopifycloud/checkout-web/assets/c1/helpers-setAddressErrors.COSrgzI4.js","/cdn/shopifycloud/checkout-web/assets/c1/types-index.Cer_moiw.js","/cdn/shopifycloud/checkout-web/assets/c1/images-flag-icon.C_eXYJRt.js","/cdn/shopifycloud/checkout-web/assets/c1/locale-en.CXVkHWV9.js","/cdn/shopifycloud/checkout-web/assets/c1/page-OnePage.B78_Z6U9.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useWalletsTimeout.sxKHMrsr.js","/cdn/shopifycloud/checkout-web/assets/c1/remember-me-hooks.BlRFIjPH.js","/cdn/shopifycloud/checkout-web/assets/c1/OffsitePaymentFailed.CXN6IhLG.js","/cdn/shopifycloud/checkout-web/assets/c1/NoAddressLocationFullDetour.DxT8ZCsI.js","/cdn/shopifycloud/checkout-web/assets/c1/SplitDeliveryMerchandiseContainer.JAVvwb9m.js","/cdn/shopifycloud/checkout-web/assets/c1/useShopPayButtonClassName.Dj35X_uD.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useCheckoutProtocolDarkTheme.geoZxhPB.js","/cdn/shopifycloud/checkout-web/assets/c1/ChangeCompanyLocationLink.BnJtkteT.js","/cdn/shopifycloud/checkout-web/assets/c1/WalletsSandbox-WalletSandbox.BrTpb1aa.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useUnauthenticatedErrorModal.d61gHRAw.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useForceShopPayUrl.CCc1WlwH.js","/cdn/shopifycloud/checkout-web/assets/c1/GooglePayButton-index.BzeDWdww.js","/cdn/shopifycloud/checkout-web/assets/c1/MarketsProDisclaimer.BtZfdTFr.js","/cdn/shopifycloud/checkout-web/assets/c1/ShippingGroupsSummaryLine.CDsHwVRR.js","/cdn/shopifycloud/checkout-web/assets/c1/StackedMerchandisePreview.BS32vHn-.js","/cdn/shopifycloud/checkout-web/assets/c1/AutocompleteField-hooks.BVRiECGL.js","/cdn/shopifycloud/checkout-web/assets/c1/LocalizationExtensionField.CdjVTQDY.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useShopPayPaymentRequiredMethod.D0fcl3Du.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useUpdateCheckoutAddress.ymjPOYMl.js","/cdn/shopifycloud/checkout-web/assets/c1/WalletLogo.DZEFiKOh.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useGeneralPaymentErrorMessage.BY22iVyK.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useShowShopPayOptin.DEGSXojV.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useShowCreateMoreAccountsGdprTreatment.DOIUNQMM.js","/cdn/shopifycloud/checkout-web/assets/c1/Section.BZ2ABfRR.js","/cdn/shopifycloud/checkout-web/assets/c1/MobileOrderSummary.DnK3Cv0O.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useOnePageFormSubmit.Dt2OJUJB.js","/cdn/shopifycloud/checkout-web/assets/c1/PayPalOverCaptureInfoBanner.2GT4tp4w.js","/cdn/shopifycloud/checkout-web/assets/c1/utilities-get-negotiation-input.CZuSkPzu.js","/cdn/shopifycloud/checkout-web/assets/c1/shop-cash-constants.D-mYWt6V.js","/cdn/shopifycloud/checkout-web/assets/c1/PaymentErrorBanner.B270B_Be.js","/cdn/shopifycloud/checkout-web/assets/c1/StockProblems-StockProblemsLineItemList.CZ_Syo_q.js","/cdn/shopifycloud/checkout-web/assets/c1/DutyOptions.DWKFx4RT.js","/cdn/shopifycloud/checkout-web/assets/c1/ShipmentBreakdown.DeyxfsPm.js","/cdn/shopifycloud/checkout-web/assets/c1/MerchandiseModal.D-47g-es.js","/cdn/shopifycloud/checkout-web/assets/c1/extension-targets-shipping-options.CXCkSM3x.js","/cdn/shopifycloud/checkout-web/assets/c1/ShippingMethodSelector.CjaA4jYB.js","/cdn/shopifycloud/checkout-web/assets/c1/SubscriptionPriceBreakdown.gEN7Pcoc.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useSubscribeMessenger.Di1TADsr.js"];
      var styles = ["/cdn/shopifycloud/checkout-web/assets/c1/assets/app.kbFPPpOR.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/useReplaceShopPayInHistory.C-ppsiYq.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/utilities.F5mjvpnu.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/FullScreenBackground.B_iZlQze.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/index.iFhC-FZy.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/OnePage.Db-FuZsA.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/SplitDeliveryMerchandiseContainer.CRDql5Io.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/LocalizationExtensionField.UsZTbb_4.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/MobileOrderSummary.CqVkJv9Z.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/useOnePageFormSubmit.BRUjVIS4.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/WalletLogo.CIy8uDiZ.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/ChangeCompanyLocationLink.uqpm88mq.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/Section.CU18S7Ap.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/useShopPayButtonClassName.Ho_Bkwiw.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/DutyOptions.LcqrKXE1.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/PayPalOverCaptureInfoBanner.CuS5ve3d.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/NoAddressLocationFullDetour.CpFaJIpx.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/WalletSandbox.CnR7qNLY.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/ShippingMethodSelector.B0hio2RO.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/SubscriptionPriceBreakdown.BSemv9tH.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/StackedMerchandisePreview.D6OuIVjc.css"];
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
  