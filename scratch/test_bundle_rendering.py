from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import json

options = Options()
options.add_argument("--headless")
options.add_argument("--allow-file-access-from-files")

print("Launching Chrome...")
driver = webdriver.Chrome(options=options)

try:
    # 1. Open the cart page
    cart_path = r"C:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\cart\index.html"
    file_url = "file:///" + cart_path.replace("\\", "/")
    print(f"Opening {file_url}...")
    driver.get(file_url)
    time.sleep(1)

    # 2. Inject cart items into localStorage
    cart_data = {
      "items": [
        {
          "productId": "cat-wellness-mix",
          "name": "Cat Wellness Mix",
          "price": 22000,
          "quantity": 1,
          "image": "products/cat-wellness-mix/images/CatWellnessMix-341.jpg",
          "slug": "cat-wellness-mix"
        },
        {
          "productId": "duck-soft-chews",
          "name": "Duck Soft Chews",
          "price": 22000,
          "quantity": 1,
          "image": "products/duck-soft-chews/images/DuckSoftChews-353.jpg",
          "slug": "duck-soft-chews"
        },
        {
          "productId": "lamb-quinoa-blend",
          "name": "Lamb Quinoa Blend",
          "price": 15000,
          "quantity": 1,
          "image": "products/lamb-quinoa-blend/images/LambQuinoaBlend-393.jpg",
          "slug": "lamb-quinoa-blend"
        }
      ]
    }
    js_inject = f"localStorage.setItem('rawjoy_cart_hybrid', '{json.dumps(cart_data)}');"
    driver.execute_script(js_inject)
    print("Injected cart items into localStorage.")

    # 3. Reload the page to render the injected cart
    driver.refresh()
    time.sleep(2)

    # 4. Verify DOM calculations
    subtotal_el = driver.find_element(By.ID, "cart-subtotal")
    discount_row = driver.find_element(By.ID, "bundle-discount-row")
    discount_val = driver.find_element(By.ID, "bundle-discount-val")
    total_el = driver.find_element(By.ID, "cart-total-amount")

    print(f"Subtotal text: {subtotal_el.text}")
    print(f"Discount row style: {discount_row.get_attribute('style')}")
    print(f"Discount val: {discount_val.text}")
    print(f"Total val: {total_el.text}")

    # Check individual item prices in the list
    item_prices = driver.find_elements(By.CLASS_INFO if hasattr(By, 'CLASS_INFO') else By.CLASS_NAME, "item-price")
    for i, ip in enumerate(item_prices):
        print(f"Item {i} price: {ip.text}")

    # Save a screenshot to verify visually
    screenshot_path = r"C:\Users\junxi\.gemini\antigravity-ide\brain\45fa12e0-5442-4e8b-99bc-427d93665aaf\verify_discount_rendering.png"
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")

finally:
    driver.quit()
