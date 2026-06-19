import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

try:
    url = "http://localhost/RawJoy/index.html"
    driver.get(url)
    print("Page Title:", driver.title)
    print("Current URL:", driver.current_url)
    
    # Evaluate getDepthPrefix, baseUrl, and resolveUrl simulation
    result = driver.execute_script("""
        function getDepthPrefix() {
            var loc = window.location.pathname;
            var parts = loc.split('/').filter(Boolean);
            var index = -1;
            for (var i = 0; i < parts.length; i++) {
                if (parts[i].toLowerCase() === 'rawjoy' || parts[i].toLowerCase() === 'homepage') {
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
            var depth = relevantParts.length;
            if (depth <= 0) return './';
            return new Array(depth + 1).join('../');
        }
        
        var prefix = getDepthPrefix();
        var folderSeparator = 'products/';
        var productId = 'chicken-bone-treat';
        var productPageUrl = prefix + folderSeparator + productId + '/';
        var baseUrl = productPageUrl.split('?')[0];
        
        function resolveUrl(relUrl) {
            if (!relUrl || relUrl.startsWith('http:') || relUrl.startsWith('https:') || relUrl.startsWith('data:')) {
                return relUrl;
            }
            if (relUrl.startsWith('/')) {
                var pathname = window.location.pathname;
                var rawjoyIndex = pathname.toLowerCase().indexOf('/rawjoy');
                if (rawjoyIndex !== -1) {
                    var subfolderPrefix = pathname.substring(0, rawjoyIndex + 8);
                    if (!relUrl.toLowerCase().startsWith(subfolderPrefix.toLowerCase())) {
                        return subfolderPrefix + relUrl.substring(1);
                    }
                }
                return relUrl;
            }
            try {
                return new URL(relUrl, new URL(baseUrl, window.location.href)).toString();
            } catch(e) {
                return relUrl + ' | Error: ' + e.message;
            }
        }
        
        return {
            windowLocationHref: window.location.href,
            windowLocationPathname: window.location.pathname,
            prefix: prefix,
            productPageUrl: productPageUrl,
            baseUrl: baseUrl,
            resolvedUrl: resolveUrl('images/ChickenBoneTreat-418.jpg')
        };
    """)
    print("JS Evaluation Result:")
    for k, v in result.items():
        print(f"  {k}: {v}")
        
finally:
    driver.quit()
