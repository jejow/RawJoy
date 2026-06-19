import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.stdout.reconfigure(encoding='utf-8')

artifacts_dir = r"C:\Users\junxi\.gemini\antigravity-ide\brain\05501510-085e-456c-87b7-71376ee9275c"
if not os.path.exists(artifacts_dir):
    artifacts_dir = r"C:\Users\junxi\._temp_artifacts"
os.makedirs(artifacts_dir, exist_ok=True)

# Launch headless browser
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

print("Launching Chrome...")
try:
    driver = webdriver.Chrome(options=options)
except Exception as e:
    print("Error launching Chrome, trying Edge...")
    from selenium.webdriver.edge.options import Options as EdgeOptions
    edge_options = EdgeOptions()
    edge_options.add_argument("--headless")
    edge_options.add_argument("--window-size=1920,1080")
    edge_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    driver = webdriver.Edge(options=edge_options)

def save_and_print_log(name):
    driver.save_screenshot(os.path.join(artifacts_dir, name))
    print(f"Saved screenshot: {name}")

try:
    # --- 1. VERIFY SEARCH FUNCTION ---
    print("\n--- 1. VERIFY SEARCH FUNCTION ---")
    product_url = "http://localhost/RawJoy/products/chicken-bone-treat/index.html"
    print(f"Navigating to: {product_url}")
    driver.get(product_url)
    time.sleep(2)
    
    # Check if there is a search trigger to click (for drawers or modals)
    try:
        search_triggers = driver.find_elements(By.CSS_SELECTOR, "summary.header__icon--search, a[aria-controls^='Details-HeaderSearch-'], .header__icon--search")
        if search_triggers and search_triggers[0].is_displayed():
            print("Clicking search trigger to expand form...")
            driver.execute_script("arguments[0].click();", search_triggers[0])
            time.sleep(0.5)
    except Exception as e:
        print(f"Note: Search trigger not clicked or not found: {e}")

    # Find search input
    search_inputs = driver.find_elements(By.CSS_SELECTOR, "input[name='q']")
    if not search_inputs:
         raise Exception("No search input field found!")
    
    search_input = None
    for inp in search_inputs:
        if inp.is_displayed():
            search_input = inp
            break
    if not search_input:
        search_input = search_inputs[0]
        
    print("Typing search query 'Stick'...")
    driver.execute_script("arguments[0].value = 'Stick';", search_input)
    # Also trigger input event for any reactive search logic
    driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", search_input)
    save_and_print_log("search_typed.png")
    
    print("Submitting search form...")
    driver.execute_script("""
        const input = arguments[0];
        const form = input.closest('form');
        if (form) {
            form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
            if (!form.defaultPrevented) {
                form.submit();
            }
        } else {
            input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true }));
        }
    """, search_input)
    time.sleep(2)
    
    current_url = driver.current_url
    print(f"Redirected URL: {current_url}")
    save_and_print_log("search_result_page.png")
    if "q=Stick" in current_url:
        print("SUCCESS: Search redirection is correct and matches index.html?q=Stick")
    else:
        print("WARNING: Search redirection URL did not contain q=Stick as expected.")


    # --- 2. VERIFY SHOPIFY LOGIN INTERCEPT ---
    print("\n--- 2. VERIFY SHOPIFY LOGIN INTERCEPT ---")
    blog_url = "http://localhost/RawJoy/blogs/news/blue-cat-portrait/index.html"
    print(f"Navigating to: {blog_url}")
    driver.get(blog_url)
    time.sleep(2)
    
    # Find account login link/button
    account_btn = None
    triggers = driver.find_elements(By.CSS_SELECTOR, ".header-account-btn, .account-trigger, a[href*='account/login'], a[href*='customer_authentication']")
    for t in triggers:
        if t.is_displayed() or t.get_attribute("href"):
            account_btn = t
            break
            
    if account_btn:
        print(f"Found account button with href: {account_btn.get_attribute('href')}. Clicking...")
        driver.execute_script("arguments[0].click();", account_btn)
        time.sleep(1.5)
        
        # Verify local custom auth modal is open
        auth_modal = driver.find_element(By.ID, "auth-modal")
        modal_class = auth_modal.get_attribute("class") or ""
        is_modal_visible = auth_modal.is_displayed() or "active" in modal_class
        print(f"Auth Modal visible/active: {is_modal_visible} (class='{modal_class}')")
        save_and_print_log("blog_login_intercept.png")
        if is_modal_visible:
            print("SUCCESS: Shopify login link successfully intercepted, local modal is open!")
        else:
            print("WARNING: Local auth modal is not open on the blog page.")
            
        # Close the modal
        try:
            close_btn = driver.find_element(By.ID, "auth-modal-close")
            if close_btn.is_displayed():
                driver.execute_script("arguments[0].click();", close_btn)
                time.sleep(0.5)
        except Exception:
            pass
    else:
        print("WARNING: Could not find account button to test login redirect intercept.")


    # --- 3. VERIFY COMPLETE THE LOOK AND IMAGES ---
    print("\n--- 3. VERIFY COMPLETE THE LOOK AND IMAGES ---")
    homepage_url = "http://localhost/RawJoy/index.html"
    print(f"Navigating to: {homepage_url}")
    driver.get(homepage_url)
    time.sleep(2)
    
    # Add a main product to initialize the cart drawer
    print("Locating a product card submit button...")
    main_submit_btns = driver.find_elements(By.CSS_SELECTOR, "button[id*='Submit'], button[name='add'], .product-card button")
    if main_submit_btns:
        main_submit_btn = main_submit_btns[0]
        print("Adding a main product to cart to initialize cart drawer...")
        driver.execute_script("arguments[0].click();", main_submit_btn)
        time.sleep(3)
    else:
        print("WARNING: No main product submit button found to open cart.")

    # Ensure cart drawer is open
    cart_drawer = driver.find_element(By.ID, "cart-drawer-dialog")
    drawer_open = cart_drawer.is_displayed() or cart_drawer.get_attribute("open") is not None
    if not drawer_open:
        print("Cart drawer not open, opening manually...")
        cart_triggers = driver.find_elements(By.CSS_SELECTOR, ".header__icon--cart, #cart-icon-bubble")
        if cart_triggers:
            driver.execute_script("arguments[0].click();", cart_triggers[0])
            time.sleep(1.5)
            
    save_and_print_log("cart_drawer_open.png")
    
    # Wait for recommended items to load asynchronously
    print("Waiting for recommended items to render...")
    time.sleep(3)
    
    # Locate Chicken Bone add button in Complete the Look
    # Complete the look cards:
    complete_look_cards = driver.find_elements(By.CSS_SELECTOR, ".complete-look-card")
    print(f"Found {len(complete_look_cards)} recommended items in Complete The Look:")
    for card in complete_look_cards:
        print(f" - {card.text.replace(chr(10), ' | ')}")
        
    chicken_bone_add = None
    recommended_name = None
    for card in complete_look_cards:
        # We can dynamically select the first available recommended item
        try:
            btn = card.find_element(By.CSS_SELECTOR, ".complete-look-add-btn, button[onclick*='-treat'], button[onclick*='-stick'], button[onclick*='-formula']")
            chicken_bone_add = btn
            recommended_name = card.find_element(By.CSS_SELECTOR, ".complete-look-name").text.strip()
            print(f"Selected recommended item for testing: '{recommended_name}'")
            break
        except Exception:
            pass
                
    if chicken_bone_add:
        print(f"Clicking recommended add button for '{recommended_name}'...")
        driver.execute_script("arguments[0].click();", chicken_bone_add)
        time.sleep(2)
        
        # Verify variant picker popup
        quick_add_dialog = driver.find_element(By.ID, "quick-add-dialog")
        dialog_class = quick_add_dialog.get_attribute("class") or ""
        is_picker_open = quick_add_dialog.is_displayed() or "open" in dialog_class or quick_add_dialog.get_attribute("open") is not None
        print(f"Variant picker popup open: {is_picker_open}")
        save_and_print_log("variant_picker_open.png")
        
        if is_picker_open:
            # Check image inside picker
            try:
                picker_img = quick_add_dialog.find_element(By.CSS_SELECTOR, "img")
                img_src = picker_img.get_attribute("src") or ""
                print(f"Picker image source URL: {img_src}")
                
                # Check naturalWidth via browser JS evaluation
                img_loaded = driver.execute_script("return arguments[0] ? (arguments[0].complete && arguments[0].naturalWidth > 0) : false;", picker_img)
                print(f"Picker image successfully loaded (non-broken): {img_loaded}")
                if img_loaded:
                    print(f"SUCCESS: Recommended Item Variant Picker image loads properly for '{recommended_name}'!")
                else:
                    print(f"WARNING: Recommended Item Variant Picker image is broken for '{recommended_name}'.")
            except Exception as e:
                print(f"WARNING: Picker image not found or failed to verify: {e}")
                
            # Select first radio option
            try:
                radio_opts = quick_add_dialog.find_elements(By.CSS_SELECTOR, "input[type='radio']")
                if radio_opts:
                    print("Selecting variant option...")
                    driver.execute_script("arguments[0].click();", radio_opts[0])
                    time.sleep(0.5)
            except Exception as e:
                print(f"Note: radio option click issue: {e}")
                
            # Click submit in variant picker
            try:
                picker_submit = quick_add_dialog.find_element(By.CSS_SELECTOR, "button[type='submit']")
                print("Clicking Add to Cart inside variant picker...")
                driver.execute_script("arguments[0].click();", picker_submit)
                time.sleep(2.5)
            except Exception as e:
                print(f"Error submitting variant picker: {e}")
                
            # Reopen cart drawer if closed
            cart_drawer = driver.find_element(By.ID, "cart-drawer-dialog")
            drawer_open = cart_drawer.is_displayed() or cart_drawer.get_attribute("open") is not None
            if not drawer_open:
                print("Reopening cart drawer...")
                cart_triggers = driver.find_elements(By.CSS_SELECTOR, ".header__icon--cart, #cart-icon-bubble")
                if cart_triggers:
                    driver.execute_script("arguments[0].click();", cart_triggers[0])
                    time.sleep(1.5)
                    
            # Check if selected recommended item is in cart and removed from Complete the Look
            items_in_cart = driver.find_elements(By.CSS_SELECTOR, ".cart-item-card, .cart-item")
            item_in_cart = False
            for item in items_in_cart:
                if recommended_name in item.text:
                    item_in_cart = True
                    break
                    
            cards_in_recommended = driver.find_elements(By.CSS_SELECTOR, ".complete-look-card")
            item_in_recommended = False
            for card in cards_in_recommended:
                if recommended_name in card.text:
                    item_in_recommended = True
                    break
                    
            print(f"'{recommended_name}' in cart: {item_in_cart}")
            print(f"'{recommended_name}' in Complete The Look recommended list: {item_in_recommended}")
            save_and_print_log("cart_drawer_after_add.png")
            
            if item_in_cart and not item_in_recommended:
                print(f"SUCCESS: '{recommended_name}' is added to cart and successfully removed from Complete The Look recommended list!")
            else:
                print(f"WARNING: '{recommended_name}' did not get filtered out of recommended list.")
        else:
            print("WARNING: Variant picker popup was not open.")
    else:
        print("WARNING: No recommended items found in Complete The Look for testing.")

    print("\nChecking browser logs for JavaScript errors...")
    logs = driver.get_log('browser')
    for entry in logs:
        print(f"[{entry['level']}] {entry['message']}")

finally:
    driver.quit()
    print("\nVerification script finished.")
