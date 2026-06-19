from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

print("Launching Chrome...")
try:
    driver = webdriver.Chrome(options=options)
except Exception as e:
    print("Error launching Chrome, trying Edge...")
    try:
        from selenium.webdriver.edge.options import Options as EdgeOptions
        edge_options = EdgeOptions()
        edge_options.add_argument("--headless")
        edge_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        driver = webdriver.Edge(options=edge_options)
    except Exception as ex:
        print("Error launching Edge:", ex)
        raise e

try:
    url = "http://localhost:8000/products/venison-peas-recipe/"
    print(f"Navigating to {url}...")
    driver.get(url)
    time.sleep(2)
    
    print("Clicking cart icon...")
    try:
        cart_icon = driver.find_element(By.CSS_SELECTOR, "a.cart-icon")
        cart_icon.click()
        time.sleep(2)
        print("Click successful!")
    except Exception as e:
        print("Could not click cart icon:", e)
        
    print("Gathering logs...")
    logs = driver.get_log('browser')
    
    log_lines = []
    for entry in logs:
        log_lines.append(f"[{entry['level']}] {entry['message']}")
        
    with open("selenium_logs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))
    print("Logs written to selenium_logs.txt")
    
    driver.save_screenshot("selenium_cart.png")
    print("Screenshot saved to selenium_cart.png")
finally:
    driver.quit()
