import os
import bs4

html_path = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\puppy-food\index.html"

with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
    soup = bs4.BeautifulSoup(f.read(), 'html.parser')

h1 = soup.find('h1')
if h1:
    print("HTML around <h1>:")
    # Print h1 and its parent
    parent = h1.parent
    if parent:
        print(parent.prettify()[:1000])
else:
    print("No <h1> found!")
