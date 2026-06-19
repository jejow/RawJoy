from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys

# Set stdout to use utf-8 encoding if possible, to avoid Windows console errors
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

options = Options()
options.add_argument("--headless")
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

print("Launching Chrome...")
driver = webdriver.Chrome(options=options)

artifacts_dir = r"C:\Users\junxi\.gemini\antigravity-ide\brain\57f46918-4819-485d-a3dd-5d807b5ebcf7"

try:
    # 1. Load the product page
    url = "http://localhost:8000/products/venison-peas-recipe/index.html"
    print(f"Navigating to {url}...")
    driver.get(url)
    time.sleep(2)
    
    # Clear cart/localStorage to ensure clean state
    print("Clearing localStorage...")
    driver.execute_script("window.localStorage.clear();")
    driver.refresh()
    time.sleep(2)
    
    driver.save_screenshot(os.path.join(artifacts_dir, "verify_variant_step0_initial.png"))
    print("Initial screenshot saved.")
    
    # Find main product information container
    print("Locating main product container...")
    main_container = driver.find_element(By.CSS_SELECTOR, ".product-information__details")
    
    # Get current price on page
    price_element = main_container.find_element(By.CSS_SELECTOR, "product-price .price-item--regular, product-price .price, .price__regular .price, .price")
    print(f"Initial price text on page: '{price_element.text}'")
    
    # 2. Select 150gr variant
    print("Searching for 150gr variant selector inside main container...")
    labels = main_container.find_elements(By.CSS_SELECTOR, "label, input[type='radio']")
    target_150gr_label = None
    target_200gr_label = None
    
    for l in labels:
        txt = l.text or l.get_attribute("value") or ""
        # Check text or attribute
        if "150gr" in txt or "150g" in txt:
            target_150gr_label = l
            print(f"Found 150gr selector: tag={l.tag_name}, text={txt}")
        elif "200gr" in txt or "200g" in txt:
            target_200gr_label = l
            print(f"Found 200gr selector: tag={l.tag_name}, text={txt}")
            
    if not target_150gr_label:
        # Fallback by variant ID
        print("Fallback search for radio inputs by value...")
        inputs = main_container.find_elements(By.CSS_SELECTOR, "input[type='radio']")
        for inp in inputs:
            val = inp.get_attribute("value")
            if val == "50657212498210":
                target_150gr_label = inp
                print(f"Found 150gr radio input: {val}")
            elif val == "50657212530978":
                target_200gr_label = inp
                print(f"Found 200gr radio input: {val}")

    # Click 150gr
    print("Clicking 150gr variant...")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_150gr_label)
    time.sleep(0.5)
    
    try:
        target_150gr_label.click()
    except Exception:
        driver.execute_script("arguments[0].click();", target_150gr_label)
        
    time.sleep(2)
    print(f"Price text on page after 150gr click: '{price_element.text}'")
    
    # 3. Add to cart
    print("Finding Add to Cart button inside main container...")
    add_btn = main_container.find_element(By.CSS_SELECTOR, "button[type='submit'], .add-to-cart-button")
    print("Clicking Add to Cart button...")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_btn)
    time.sleep(0.5)
    try:
        add_btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", add_btn)
        
    time.sleep(3)
    
    driver.save_screenshot(os.path.join(artifacts_dir, "verify_variant_step1_cart_150gr.png"))
    print("Cart 150gr screenshot saved.")
    
    # Print cart drawer content
    try:
        drawer = driver.find_element(By.CSS_SELECTOR, "#cart-drawer-dialog, .cart-drawer")
        print("Cart Drawer Text:")
        print(drawer.text)
    except Exception as e:
        print("Could not find cart drawer:", e)
        
    # Close cart drawer
    print("Closing cart drawer...")
    try:
        close_btn = driver.find_element(By.CSS_SELECTOR, ".cart-drawer__close, #cart-drawer-dialog button.close, [aria-label='Close']")
        close_btn.click()
    except Exception:
        driver.execute_script("document.getElementById('cart-drawer-dialog').close();")
    time.sleep(1)
    
    # 4. Select 200gr variant
    print("Clicking 200gr variant...")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_200gr_label)
    time.sleep(0.5)
    try:
        target_200gr_label.click()
    except Exception:
        driver.execute_script("arguments[0].click();", target_200gr_label)
        
    time.sleep(2)
    print(f"Price text on page after 200gr click: '{price_element.text}'")
    
    # Add to cart
    print("Clicking Add to Cart button...")
    try:
        add_btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", add_btn)
        
    time.sleep(3)
    driver.save_screenshot(os.path.join(artifacts_dir, "verify_variant_step2_cart_200gr.png"))
    print("Cart 200gr screenshot saved.")
    
    try:
        drawer = driver.find_element(By.CSS_SELECTOR, "#cart-drawer-dialog, .cart-drawer")
        print("Updated Cart Drawer Text:")
        print(drawer.text)
    except Exception as e:
        print("Could not find cart drawer:", e)
        
    # 5. Go to checkout
    print("Clicking checkout button...")
    checkout_btn = driver.find_element(By.CSS_SELECTOR, "button[name='checkout'], a[href*='/checkout'], button.cart-drawer__checkout")
    try:
        checkout_btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", checkout_btn)
        
    time.sleep(3)
    driver.save_screenshot(os.path.join(artifacts_dir, "verify_variant_step3_checkout.png"))
    print("Checkout page screenshot saved.")
    
    try:
        checkout_body = driver.find_element(By.CSS_SELECTOR, "body")
        print("Checkout Page Text:")
        for line in checkout_body.text.split('\n'):
            if "Venison Peas" in line or "$" in line or "Total" in line:
                print(f"  {line}")
    except Exception as e:
        print("Could not get checkout text:", e)

    print("\nGathering console logs...")
    logs = driver.get_log('browser')
    log_lines = []
    for entry in logs:
        msg = f"[{entry['level']}] {entry['message']}"
        log_lines.append(msg)
        # Safely print msg using ascii replacement for console
        safe_msg = msg.encode('ascii', 'replace').decode('ascii')
        print(safe_msg)

    with open("selenium_variants_logs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))
    print("Full logs written to selenium_variants_logs.txt")

except Exception as e:
    print(f"Error occurred during test execution: {e}")
    import traceback
    traceback.print_exc()
finally:
    driver.quit()
