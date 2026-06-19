import urllib.request
import os

url = "http://pebble-rawjoy.myshopify.com/cdn/shop/t/2/assets/section-renderer.js"
target_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\scratch\section-renderer.js"

try:
    print(f"Downloading from {url}...")
    urllib.request.urlretrieve(url, target_path)
    print("Success! File size:", os.path.getsize(target_path))
except Exception as e:
    print("Error:", e)
