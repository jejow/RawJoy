import os
import sys
from playwright.sync_api import sync_playwright

artifacts_dir = r"C:\Users\junxi\._temp_artifacts" if not os.path.exists(r"C:\Users\junxi\.gemini\antigravity-ide\brain\05501510-085e-456c-87b7-71376ee9275c") else r"C:\Users\junxi\.gemini\antigravity-ide\brain\05501510-085e-456c-87b7-71376ee9275c"
os.makedirs(artifacts_dir, exist_ok=True)

def verify():
    with sync_playwright() as p:
        # Launch browser in non-headless mode if you want, but headless is safer/faster
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Capture console logs
        page.on("console", lambda msg: print(f"[Browser Console] {msg.type}: {msg.text}"))

        print("\n--- 1. VERIFY SEARCH FUNCTION ---")
        # Go to product page
        product_url = "http://localhost/RawJoy/products/chicken-bone-treat/index.html"
        print(f"Navigating to: {product_url}")
        page.goto(product_url)
        page.wait_for_load_state("networkidle")
        
        # Click search icon to open search drawer if needed
        # Let's search for search icon/summary and click it
        search_trigger = page.locator("summary.header__icon--search, a[aria-controls='Details-HeaderSearch-sections--26013853417762__header'], .header__icon--search").first
        if search_trigger.is_visible():
            print("Clicking search trigger to open search drawer...")
            search_trigger.click()
            page.wait_for_timeout(500)
            
        # Find search input and type query
        search_input = page.locator("input[name='q']").first
        print("Typing search query 'Stick'...")
        search_input.fill("Stick")
        page.screenshot(path=os.path.join(artifacts_dir, "search_typed.png"))
        
        # Submit form
        print("Submitting search form...")
        search_input.press("Enter")
        page.wait_for_timeout(2000)
        
        # Verify redirect url
        current_url = page.url
        print(f"Redirected URL: {current_url}")
        page.screenshot(path=os.path.join(artifacts_dir, "search_result_page.png"))
        if "q=Stick" in current_url:
            print("SUCCESS: Search redirection is correct and matches index.html?q=Stick")
        else:
            print("WARNING: Search redirection URL did not contain q=Stick as expected.")

        print("\n--- 2. VERIFY SHOPIFY LOGIN INTERCEPT ---")
        # Go to blog page
        blog_url = "http://localhost/RawJoy/blogs/news/blue-cat-portrait/index.html"
        print(f"Navigating to: {blog_url}")
        page.goto(blog_url)
        page.wait_for_load_state("networkidle")
        
        # Click account button
        account_btn = page.locator(".header-account-btn, .account-trigger, a[href*='account/login']").first
        print("Clicking account button...")
        account_btn.click()
        page.wait_for_timeout(1000)
        
        # Check if auth modal is open and active
        auth_modal = page.locator("#auth-modal")
        is_modal_visible = auth_modal.is_visible() or "active" in (auth_modal.get_attribute("class") or "")
        print(f"Auth Modal visible/active: {is_modal_visible}")
        page.screenshot(path=os.path.join(artifacts_dir, "blog_login_intercept.png"))
        if is_modal_visible:
            print("SUCCESS: Shopify login link successfully intercepted, local modal is open!")
        else:
            print("WARNING: Local auth modal is not open on the blog page.")
            
        # Close modal
        close_btn = page.locator("#auth-modal-close")
        if close_btn.is_visible():
            close_btn.click()
            page.wait_for_timeout(500)

        print("\n--- 3. VERIFY COMPLETE THE LOOK AND IMAGES ---")
        # Go to homepage
        homepage_url = "http://localhost/RawJoy/index.html"
        print(f"Navigating to: {homepage_url}")
        page.goto(homepage_url)
        page.wait_for_load_state("networkidle")
        
        # Add a product to cart first if cart is empty
        # Click the add button on first product card
        add_to_cart_btn = page.locator("button[id*='Submit'], button[name='add'], .product-card button").first
        print("Adding a main product to cart to initialize cart drawer...")
        add_to_cart_btn.click()
        page.wait_for_timeout(1500)
        
        # Ensure cart drawer is open
        cart_drawer = page.locator("#cart-drawer-dialog")
        if not (cart_drawer.is_visible() or "open" in (cart_drawer.get_attribute("open") or "")):
            print("Opening cart drawer manually...")
            page.locator(".header__icon--cart, #cart-icon-bubble").first.click()
            page.wait_for_timeout(1000)
            
        # Check Complete The Look items
        print("Cart Drawer is open. Checking recommended items in 'Complete The Look'...")
        page.screenshot(path=os.path.join(artifacts_dir, "cart_drawer_open.png"))
        
        # Find 'Chicken Bone' add button in Complete The Look
        # Selector for the add button on Chicken Bone card
        chicken_bone_add = page.locator(".complete-look-card:has-text('Chicken Bone') .complete-look-add-btn, button[onclick*='chicken-bone-treat']").first
        if chicken_bone_add.is_visible():
            print("Clicking add button on Chicken Bone recommended item...")
            chicken_bone_add.click()
            page.wait_for_timeout(1500)
            
            # Verify option picker modal is open
            quick_add_dialog = page.locator("#quick-add-dialog")
            is_picker_open = quick_add_dialog.is_visible() or "open" in (quick_add_dialog.get_attribute("open") or "")
            print(f"Variant picker popup open: {is_picker_open}")
            
            # Check image inside picker
            picker_img = page.locator("#quick-add-dialog img").first
            img_src = picker_img.get_attribute("src") or ""
            print(f"Picker image source URL: {img_src}")
            
            # Check if image loaded (naturalWidth > 0 in browser context)
            img_loaded = page.evaluate("el => el ? el.complete && el.naturalWidth > 0 : false", picker_img.element_handle())
            print(f"Picker image successfully loaded: {img_loaded}")
            page.screenshot(path=os.path.join(artifacts_dir, "variant_picker_open.png"))
            
            # Select first radio option (e.g. 100gr)
            radio_opt = page.locator("#quick-add-dialog input[type='radio']").first
            if radio_opt.is_visible():
                print("Selecting variant option...")
                radio_opt.click()
                page.wait_for_timeout(500)
                
            # Click Add to Cart button in variant picker
            picker_submit = page.locator("#quick-add-dialog button[type='submit']").first
            print("Clicking Add to Cart inside variant picker...")
            picker_submit.click()
            page.wait_for_timeout(2000)
            
            # Reopen cart drawer if closed
            if not (cart_drawer.is_visible() or "open" in (cart_drawer.get_attribute("open") or "")):
                print("Reopening cart drawer...")
                page.locator(".header__icon--cart, #cart-icon-bubble").first.click()
                page.wait_for_timeout(1000)
                
            # Verify if Chicken Bone is now in cart and NOT in Complete The Look
            chicken_bone_in_cart = page.locator(".cart-item-card:has-text('Chicken Bone')").is_visible()
            chicken_bone_in_recommended = page.locator(".complete-look-card:has-text('Chicken Bone')").is_visible()
            
            print(f"Chicken Bone in cart: {chicken_bone_in_cart}")
            print(f"Chicken Bone in Complete The Look recommended list: {chicken_bone_in_recommended}")
            page.screenshot(path=os.path.join(artifacts_dir, "cart_drawer_after_add.png"))
            
            if chicken_bone_in_cart and not chicken_bone_in_recommended:
                print("SUCCESS: Chicken Bone is added to cart and successfully removed from Complete The Look recommended list!")
            else:
                print("WARNING: Complete The Look item did not get filtered out of recommended list.")
        else:
            print("WARNING: Chicken Bone recommended item not found in Complete The Look.")

        browser.close()

if __name__ == "__main__":
    verify()
