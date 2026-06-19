from bs4 import BeautifulSoup

filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections\air-dried-food\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')
nav = soup.find('nav', class_='pagination')
if nav:
    print(str(nav))
else:
    print("No pagination nav found")
