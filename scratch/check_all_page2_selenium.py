from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

collections_to_check = [
    "puppy-food-1",
    "wet-food-1",
    "colostrum-1",
    "supplements-1",
    "air-dried-food-1",
    "cat-food-1",
    "freeze-dried-1",
    "sockete-salmon-1"
]

def check_collection(name):
    url = f"http://localhost:8000/collections/{name}/index.html"
    print(f"\nChecking: {url}")
    try:
        driver.get(url)
        time.sleep(2)
        
        # Scroll to bottom to trigger lazy loading
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        items = driver.find_elements(By.CSS_SELECTOR, "li.product-grid__item")
        print(f"  Total product cards: {len(items)}")
        
        broken_count = 0
        for idx, item in enumerate(items):
            try:
                title = item.find_element(By.CSS_SELECTOR, ".product-card__title").text.strip()
            except Exception:
                title = f"Unknown product at index {idx}"
                
            imgs = item.find_elements(By.CSS_SELECTOR, "img")
            if not imgs:
                print(f"   - [NO IMG TAG] {title}")
                broken_count += 1
                continue
                
            for img in imgs:
                src = img.get_attribute("src")
                is_loaded = driver.execute_script(
                    "return arguments[0].complete && typeof arguments[0].naturalWidth != 'undefined' && arguments[0].naturalWidth > 0;", 
                    img
                )
                if not is_loaded:
                    print(f"   - [BROKEN IMG] {title}")
                    print(f"     src: {src}")
                    broken_count += 1
        
        if broken_count == 0:
            print("  All images loaded successfully!")
        else:
            print(f"  Found {broken_count} issues with images.")
            
    except Exception as e:
        print(f"  Error checking {name}: {e}")

try:
    for name in collections_to_check:
        check_collection(name)
finally:
    driver.quit()
