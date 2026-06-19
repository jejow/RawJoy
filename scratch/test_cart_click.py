from playwright.sync_api import sync_playwright
import time
import os

logs = []

def handle_console(msg):
    logs.append(f"[{msg.type}] {msg.text}")

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("console", handle_console)
        page.on("pageerror", lambda err: logs.append(f"[EXCEPTION] {err.message}"))
        
        url = 'http://localhost:8000/products/venison-peas-recipe/'
        print(f"Navigating to {url}...")
        page.goto(url)
        page.wait_for_load_state('networkidle')
        time.sleep(1)
        
        print("Clicking cart button...")
        cart_button = page.locator('a.cart-icon')
        if cart_button.count() > 0:
            cart_button.first.click()
            time.sleep(2)
            page.screenshot(path='cart_click_test.png')
            print("Screenshot saved to cart_click_test.png")
        else:
            print("Cart button not found!")
            
        browser.close()

    log_path = "console_logs.txt"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(logs))
    print(f"Console logs written to {log_path}")

if __name__ == "__main__":
    run()
