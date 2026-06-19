from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

try:
    url = "http://localhost:8000/"
    driver.get(url)
    time.sleep(2)
    
    # Print header HTML or elements
    header = driver.find_element(By.CSS_SELECTOR, "header")
    print("Header outer HTML:")
    print(header.get_attribute("outerHTML")[:2000]) # Print first 2000 chars of header
    
    print("\nLinks in header:")
    links = header.find_elements(By.CSS_SELECTOR, "a")
    for idx, link in enumerate(links):
        print(f"Link {idx}: tag={link.tag_name}, class={link.get_attribute('class')}, href={link.get_attribute('href')}, html={link.get_attribute('outerHTML')[:200]}")
finally:
    driver.quit()
