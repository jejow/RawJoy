from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")
# Disable cache options
options.add_argument("--disk-cache-size=1")
options.add_argument("--media-cache-size=1")
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

print("Launching Chrome with clean cache...")
driver = webdriver.Chrome(options=options)

# Use Chrome DevTools Protocol to clear cache and disable caching
driver.execute_cdp_cmd('Network.clearBrowserCache', {})
driver.execute_cdp_cmd('Network.setCacheDisabled', {'cacheDisabled': True})

try:
    url = "http://localhost:8000/index.html"
    print(f"Navigating to {url}...")
    driver.get(url)
    time.sleep(3)
    
    print("\nGathering logs...")
    logs = driver.get_log('browser')
    for entry in logs:
        msg = entry['message'].encode('ascii', errors='replace').decode('ascii')
        print(f"[{entry['level']}] {msg}")
        
    print("\nChecking if theme.js is loaded and running...")
    # theme.js defines custom elements like basic-header or sticky-header. Let's check if they are defined.
    is_defined = driver.execute_script("return typeof customElements.get('sticky-header') !== 'undefined'")
    print(f"Is custom element 'sticky-header' registered? {is_defined}")
    
finally:
    driver.quit()
