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
    
    print("Clicking Cart Icon button in header...")
    try:
        cart_button = driver.find_element(By.CSS_SELECTOR, "a.cart-icon")
        print("Found cart button. Scrolling into view...")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cart_button)
        time.sleep(1)
        cart_button.click()
        print("Click successful! Waiting for cart drawer to open...")
        time.sleep(3)
    except Exception as e:
        print("Could not click cart icon button:", e)
        
    print("Gathering logs...")
    logs = driver.get_log('browser')
    
    log_lines = []
    for entry in logs:
        log_lines.append(f"[{entry['level']}] {entry['message']}")
        
    with open("selenium_homepage_logs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))
    print("Logs written to selenium_homepage_logs.txt")
    
    driver.save_screenshot("selenium_homepage_cart.png")
    print("Screenshot saved to selenium_homepage_cart.png")
finally:
    driver.quit()
