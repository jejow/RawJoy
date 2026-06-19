from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

try:
    url = "http://localhost:8000/collections/puppy-food-1/index.html"
    print(f"Loading URL: {url}")
    driver.get(url)
    time.sleep(2)
    
    # Scroll to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    
    items = driver.find_elements(By.CSS_SELECTOR, "li.product-grid__item")
    print(f"Total product cards: {len(items)}")
    
    for idx, item in enumerate(items):
        try:
            title = item.find_element(By.CSS_SELECTOR, ".product-card__title").text.strip()
        except Exception:
            title = "Unknown product"
            
        imgs = item.find_elements(By.CSS_SELECTOR, "img")
        print(f"\n[{idx+1}] Product: {title}")
        
        if not imgs:
            print("  - [NO IMG TAG]")
            continue
            
        for img in imgs:
            src = img.get_attribute("src")
            srcset = img.get_attribute("srcset")
            
            # Use execute_script to check if the image has loaded
            is_complete = driver.execute_script("return arguments[0].complete;", img)
            natural_width = driver.execute_script("return arguments[0].naturalWidth;", img)
            
            print(f"  - img element found")
            print(f"    src: {src}")
            print(f"    complete: {is_complete}")
            print(f"    naturalWidth: {natural_width}")
            if not is_complete or (natural_width == 0):
                print("    -> [IMAGE IS BROKEN/NOT LOADED]")
                
except Exception as e:
    print(f"Error occurred: {e}")
finally:
    driver.quit()
