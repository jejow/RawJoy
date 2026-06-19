import re

file_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\Android App\pets food\full download\search\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's see if there is any pre-rendered predictive search results HTML or section in it
# Or let's see how search results are structured in this file.
# E.g. search for id="PredictiveSearchResults"
matches = re.finditer(r'(<div[^>]*id="PredictiveSearchResults[^"]*"[^>]*>.*?</div>)', content, re.DOTALL)
results = list(matches)
print(f"Found PredictiveSearchResults div: {len(results)}")
for r in results[:5]:
    print(r.group(1)[:500])
    print("=" * 60)
