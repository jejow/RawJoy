from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

# We want to inject a script at the very beginning of the page load.
# Chrome DevTools Protocol allows us to run a script on every document creation!
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': """
    window.capturedErrors = [];
    window.onerror = function(message, source, lineno, colno, error) {
        window.capturedErrors.push({
            message: message,
            source: source,
            lineno: lineno,
            colno: colno,
            stack: error ? error.stack : null
        });
        return false;
    };
    window.addEventListener('unhandledrejection', function(event) {
        window.capturedErrors.push({
            message: 'Unhandled Promise Rejection: ' + event.reason,
            source: null,
            lineno: null,
            colno: null,
            stack: event.reason ? event.reason.stack : null
        });
    });
    """
})

try:
    url = "http://localhost:8000/products/venison-peas-recipe/index.html"
    print(f"Navigating to {url}...")
    driver.get(url)
    time.sleep(3)
    
    print("\nRetrieving captured errors:")
    errors = driver.execute_script("return window.capturedErrors;")
    import json
    print(json.dumps(errors, indent=2))
    
    print("\nAlso checking browser console logs:")
    logs = driver.get_log('browser')
    for entry in logs:
        msg = entry['message'].encode('ascii', errors='replace').decode('ascii')
        print(f"[{entry['level']}] {msg}")

finally:
    driver.quit()
