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
    url = "http://localhost:8000/"
    print(f"Navigating to {url}...")
    driver.get(url)
    time.sleep(2)
    
    # Let's find all Add to Cart buttons on the homepage
    print("Finding Add to Cart buttons...")
    add_buttons = driver.find_elements(By.CSS_SELECTOR, "add-to-cart-component button, button.quick-add__button--add")
    print(f"Found {len(add_buttons)} buttons.")
    
    target_btn = None
    for idx, btn in enumerate(add_buttons):
        is_disp = btn.is_displayed()
        print(f"Button {idx}: displayed={is_disp}, html={btn.get_attribute('outerHTML')[:100]}")
        if is_disp and not target_btn:
            target_btn = btn
            
    if target_btn:
        print("Scrolling visible Add to Cart button into view...")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_btn)
        time.sleep(1)
        print("Clicking Add to Cart button...")
        target_btn.click()
        print("Click successful! Waiting for cart drawer to open...")
        time.sleep(4)
    else:
        print("No visible Add to Cart buttons found on homepage!")
        
    print("Gathering logs...")
    logs = driver.get_log('browser')
    
    log_lines = []
    for entry in logs:
        log_lines.append(f"[{entry['level']}] {entry['message']}")
        
    with open("selenium_homepage_add_logs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))
    print("Logs written to selenium_homepage_add_logs.txt")
    
    driver.save_screenshot("selenium_homepage_after_add.png")
    print("Screenshot saved to selenium_homepage_after_add.png")
finally:
    driver.quit()
