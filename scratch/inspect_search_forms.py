import os
import bs4

workspace_root = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy"
index_path = os.path.join(workspace_root, "index.html")

with open(index_path, "r", encoding="utf-8", errors="ignore") as f:
    soup = bs4.BeautifulSoup(f.read(), "html.parser")

# Search for any form tag
forms = soup.find_all("form")
print(f"Total forms found: {len(forms)}")

search_forms = []
for form in forms:
    action = form.get("action", "")
    role = form.get("role", "")
    if "search" in action.lower() or "search" in role.lower() or form.find("input", type="search") or form.find(attrs={"name": "q"}):
        search_forms.append(form)

print(f"Search forms found: {len(search_forms)}")
for idx, form in enumerate(search_forms):
    print(f"[{idx}]: action={repr(form.get('action'))} | role={repr(form.get('role'))} | id={repr(form.get('id'))}")
    # Print outer HTML of form (truncated)
    print(str(form)[:500])
    print("-" * 50)
