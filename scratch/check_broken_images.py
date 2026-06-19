from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

options = Options()
options.add_argument("--headless")

print("Launching Chrome...")
driver = webdriver.Chrome(options=options)

def check_collection(url):
    print(f"\nChecking collection: {url}")
    driver.get(url)
    time.sleep(2)
    
    # Let's scroll down to trigger lazy loading of images
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

    items = driver.find_elements(By.CSS_SELECTOR, "li.product-grid__item")
    print(f"Total product cards: {len(items)}")
    
    broken_count = 0
    for idx, item in enumerate(items):
        try:
            title = item.find_element(By.CSS_SELECTOR, ".product-card__title").text.strip()
        except Exception:
            title = f"Unknown product at index {idx}"
            
        imgs = item.find_elements(By.CSS_SELECTOR, "img")
        if not imgs:
            print(f" - [NO IMG TAG] {title}")
            broken_count += 1
            continue
            
        for img in imgs:
            src = img.get_attribute("src")
            # Check if image is loaded successfully in browser
            is_loaded = driver.execute_script(
                "return arguments[0].complete && typeof arguments[0].naturalWidth != 'undefined' && arguments[0].naturalWidth > 0;", 
                img
            )
            if not is_loaded:
                print(f" - [BROKEN IMG] Product: {title}")
                print(f"   Image tag src: {src}")
                print(f"   Image tag srcset: {img.get_attribute('srcset')}")
                broken_count += 1
                
    if broken_count == 0:
        print("All product images loaded successfully!")
    else:
        print(f"Found {broken_count} issues with images.")

try:
    check_collection("http://localhost:8000/collections/all/index.html")
    check_collection("http://localhost:8000/collections/shop-all/index.html")
finally:
    driver.quit()
