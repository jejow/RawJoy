import os

filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html"
print("File exists:", os.path.exists(filepath))
if os.path.exists(filepath):
    print("Size:", os.path.getsize(filepath))
    
    # Try different encodings
    encodings = ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'latin-1']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                content = f.read(500)
                print(f"\n--- Encoding: {enc} ---")
                print(content[:300])
        except Exception as e:
            print(f"Failed {enc}: {e}")
