import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")

print("Launching Chrome...")
driver = webdriver.Chrome(options=options)

try:
    url = "http://localhost/RawJoy/index.html"
    print(f"Navigating to {url}...")
    driver.get(url)
    time.sleep(2)
    
    print("Initial Cart Item Count (bubble):")
    bubbles = driver.find_elements(By.CSS_SELECTOR, ".cart-bubble__text-count, #cart-icon-bubble")
    for b in bubbles:
        if b.is_displayed():
            print(f" - Bubble text: '{b.text}'")

    print("Locating product card buttons...")
    btns = driver.find_elements(By.CSS_SELECTOR, "button[id*='Submit'], button[name='add'], .product-card button")
    print(f"Found {len(btns)} buttons.")
    for idx, b in enumerate(btns):
        print(f" Button {idx}: tag={b.tag_name}, text='{b.text}', id='{b.get_attribute('id')}', name='{b.get_attribute('name')}', class='{b.get_attribute('class')}'")

    if btns:
        print("Clicking first button...")
        driver.execute_script("arguments[0].click();", btns[0])
        time.sleep(3)
        
        # Verify cart drawer
        cart_drawer = driver.find_element(By.ID, "cart-drawer-dialog")
        print(f"Cart Drawer displayed: {cart_drawer.is_displayed()}")
        print(f"Cart Drawer open attr: {cart_drawer.get_attribute('open')}")
        print("\nCart Drawer Inner Text:")
        print("--------------------")
        print(cart_drawer.text)
        print("--------------------")
        
        # Print list of complete-look-card texts
        look_cards = driver.find_elements(By.CSS_SELECTOR, ".complete-look-card")
        print(f"Found {len(look_cards)} recommended items:")
        for idx, card in enumerate(look_cards):
            print(f" - Recommended {idx}: '{card.text.replace(chr(10), ' | ')}'")
            
        driver.save_screenshot("debug_cart_drawer.png")
        print("Saved screenshot: debug_cart_drawer.png")
    else:
        print("No product buttons found on the homepage!")

finally:
    driver.quit()
