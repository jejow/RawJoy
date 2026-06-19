from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

try:
    url = "http://localhost:8000/index.html"
    driver.get(url)
    time.sleep(2)
    
    # Let's execute Javascript to check if any script tag returns HTML
    js_code = """
    (async () => {
      const scripts = Array.from(document.querySelectorAll('script[src]'))
        .map(s => s.getAttribute('src'));
      const results = [];
      for (const src of scripts) {
        try {
          const resp = await fetch(src);
          const text = await resp.text();
          if (text.trim().startsWith('<')) {
            results.push({ src, status: resp.status, contentType: resp.headers.get('content-type'), textStart: text.trim().substring(0, 100) });
          }
        } catch (err) {
          results.push({ src, error: err.message });
        }
      }
      return results;
    })()
    """
    results = driver.execute_async_script("const callback = arguments[arguments.length - 1]; " + js_code + ".then(callback);")
    print("Local scripts returning HTML:")
    print(json.dumps(results, indent=2))
    
    # Check importmap targets
    js_code_importmap = """
    (async () => {
      const importmapEl = document.querySelector('script[type="importmap"]');
      if (!importmapEl) return "No importmap";
      const importmap = JSON.parse(importmapEl.textContent);
      const imports = importmap.imports || {};
      const results = [];
      for (const [key, url] of Object.entries(imports)) {
        try {
          const resp = await fetch(url);
          const text = await resp.text();
          if (text.trim().startsWith('<')) {
            results.push({ key, url, status: resp.status, contentType: resp.headers.get('content-type'), textStart: text.trim().substring(0, 100) });
          }
        } catch (err) {
          results.push({ key, url, error: err.message });
        }
      }
      return results;
    })()
    """
    results_importmap = driver.execute_async_script("const callback = arguments[arguments.length - 1]; " + js_code_importmap + ".then(callback);")
    print("\nImportmap targets returning HTML:")
    print(json.dumps(results_importmap, indent=2))

finally:
    driver.quit()
