import os
from bs4 import BeautifulSoup

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
index_path = os.path.join(workspace_root, "index.html")

with open(index_path, "r", encoding="utf-8", errors="ignore") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

# Find all form elements
forms = soup.find_all("form")
print(f"Found {len(forms)} forms in index.html:")
for idx, form in enumerate(forms):
    action = form.get("action", "")
    method = form.get("method", "")
    form_id = form.get("id", "")
    form_class = form.get("class", "")
    
    # Check if this looks like a search form
    inputs = form.find_all("input")
    input_names = [inp.get("name", "") for inp in inputs]
    
    if "q" in input_names or "search" in action or "search" in str(form_class).lower() or "search" in form_id.lower():
        print(f"Form [{idx}]: (SEARCH FORM)")
    else:
        print(f"Form [{idx}]:")
        
    print(f"  ID: {form_id}")
    print(f"  Class: {form_class}")
    print(f"  Action: {action}")
    print(f"  Method: {method}")
    print(f"  Inputs: {input_names}")
    print("-" * 40)
