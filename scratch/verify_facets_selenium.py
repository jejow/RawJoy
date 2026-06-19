from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

options = Options()
options.add_argument("--headless")
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

print("Launching Chrome...")
try:
    driver = webdriver.Chrome(options=options)
except Exception as e:
    print("Error launching Chrome, trying Edge...")
    from selenium.webdriver.edge.options import Options as EdgeOptions
    edge_options = EdgeOptions()
    edge_options.add_argument("--headless")
    edge_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    driver = webdriver.Edge(options=edge_options)

def get_visible_products():
    grid = driver.find_element(By.CSS_SELECTOR, ".product-grid")
    items = grid.find_elements(By.CSS_SELECTOR, "li.product-grid__item")
    visible = []
    for item in items:
        # Check if displayed
        if item.is_displayed():
            try:
                title = item.find_element(By.CSS_SELECTOR, ".product-card__title").text.strip()
            except Exception:
                title = "Unknown Title"
            try:
                price_el = item.find_element(By.CSS_SELECTOR, ".price-container .price--sale, .price-container .price, .price")
                price = price_el.text.strip()
            except Exception:
                price = "Unknown Price"
            visible.append((title, price))
    return visible

def print_products(title):
    print(f"\n======================================")
    print(title)
    print(f"======================================")
    products = get_visible_products()
    print(f"Total visible products: {len(products)}")
    for name, price in products:
        print(f" - {name} ({price})")
    return products

try:
    # 1. Navigate to collections/all
    url = "http://localhost:8000/collections/all/index.html"
    print(f"Navigating to {url}...")
    driver.get(url)
    time.sleep(2)
    print_products("Phase 1: Initial Default State")
    driver.save_screenshot("verify_phase_1.png")

    # 2. Check 150gr size checkbox
    print("\nChecking '150gr' size checkbox...")
    cb = driver.find_element(By.ID, "Filter-filter-v-t-shopify-accessory-size-2")
    # Use javascript click to avoid scroll-to issues
    driver.execute_script("arguments[0].click();", cb)
    time.sleep(2)
    print_products("Phase 2: After filtering by '150gr'")
    driver.save_screenshot("verify_phase_2.png")

    # 3. Sort by Price, low to high
    print("\nSorting by 'Price, low to high'...")
    select_el = driver.find_element(By.CSS_SELECTOR, ".sorting-filter__select")
    driver.execute_script("arguments[0].value = 'price-ascending'; arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", select_el)
    time.sleep(2)
    print_products("Phase 3: After sorting by Price Low-High")
    driver.save_screenshot("verify_phase_3.png")

    # 4. Set max price filter to 15.00
    print("\nSetting max price input to '15.00'...")
    driver.execute_script("""
        const el = document.getElementById('Price-LTE') || document.getElementById('Price-LTE-in-drawer');
        if (el) {
            el.value = '15.00';
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }
    """)
    time.sleep(2)
    print_products("Phase 4: After filtering max price <= 15.00")
    driver.save_screenshot("verify_phase_4.png")

    # 5. Navigate to colostrum
    url_col = "http://localhost:8000/collections/colostrum/index.html"
    print(f"\nNavigating to {url_col}...")
    driver.get(url_col)
    time.sleep(2)
    print_products("Phase 5: Colostrum initial page")
    
    # Check pagination elements
    pagination = driver.find_elements(By.CSS_SELECTOR, ".pagination")
    if pagination and pagination[0].is_displayed():
        pag_links = pagination[0].find_elements(By.CSS_SELECTOR, ".pagination__item")
        print(f"Pagination is visible. Pages shown: {[link.text.strip() for link in pag_links if link.text.strip()]}")
    else:
        print("No pagination visible initially.")
    driver.save_screenshot("verify_phase_5.png")

    # 6. Click '150gr' on colostrum page
    print("\nChecking '150gr' on Colostrum collection page...")
    cb_col = driver.find_element(By.ID, "Filter-filter-v-t-shopify-accessory-size-2")
    driver.execute_script("arguments[0].click();", cb_col)
    time.sleep(2)
    print_products("Phase 6: Colostrum after filtering by '150gr'")
    
    pagination = driver.find_elements(By.CSS_SELECTOR, ".pagination")
    if pagination and pagination[0].is_displayed():
        pag_links = pagination[0].find_elements(By.CSS_SELECTOR, ".pagination__item")
        print(f"Pagination is still visible. Pages shown: {[link.text.strip() for link in pag_links if link.text.strip()]}")
    else:
        print("No pagination visible after filter (products fit on single page).")
    driver.save_screenshot("verify_phase_6.png")

    # 7. Click Page 2 pagination link
    print("\nClicking Page 2 link on Colostrum collection page...")
    try:
        page2_link = driver.find_element(By.XPATH, "//a[contains(@class, 'pagination__item') and .//span[text()='2']] | //a[contains(@class, 'pagination__item') and text()='2']")
        driver.execute_script("arguments[0].click();", page2_link)
        time.sleep(2)
        print_products("Phase 7: Colostrum page 2 after pagination click")
        driver.save_screenshot("verify_phase_7.png")
    except Exception as e:
        print("Could not click Page 2 pagination link:", e)

    print("\nChecking browser logs for JavaScript errors...")
    logs = driver.get_log('browser')
    for entry in logs:
        print(f"[{entry['level']}] {entry['message']}")

finally:
    driver.quit()
    print("\nVerification script finished.")
