from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

print("Launching Chrome...")
driver = webdriver.Chrome(options=options)

try:
    url = "http://localhost:8000/index.html"
    print(f"Navigating to {url}...")
    driver.get(url)
    time.sleep(2)
    
    print("Refreshing page...")
    driver.refresh()
    time.sleep(3)
    
    print("Gathering logs...")
    logs = driver.get_log('browser')
    for entry in logs:
        # Avoid UnicodeEncodeError on Windows console
        msg = entry['message'].encode('ascii', errors='replace').decode('ascii')
        print(f"[{entry['level']}] {msg}")
        
    print("Saving screenshot...")
    driver.save_screenshot("selenium_homepage_refresh_debug.png")
    
    print("Checking if any elements contain raw HTML...")
    elements = driver.find_elements(By.XPATH, "//*[contains(text(), '<') or contains(text(), '{{')]")
    for el in elements:
        try:
            tag = el.tag_name
            text = el.text
            if "<" in text or "{{" in text:
                print(f"FOUND RAW HTML/TEMPLATE in tag <{tag}>: {text[:100]}")
        except Exception:
            pass

    print("Checking cart drawer dialog display style...")
    dialog = driver.find_element(By.ID, "cart-drawer-dialog")
    print("Dialog display:", dialog.get_attribute("style"))
    print("Dialog is_displayed:", dialog.is_displayed())
    print("Dialog outerHTML first 500 chars:", driver.execute_script("return arguments[0].outerHTML;", dialog)[:500])

finally:
    driver.quit()
