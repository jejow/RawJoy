filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("products/cat-calming-formula")
if idx != -1:
    card_html = content[idx:idx+15000]
    print("Length of card HTML block:", len(card_html))
    # Let's find occurrences of currency indicators or numbers
    import re
    # find something like $xx.xx or numbers
    matches = re.findall(r'(\$[0-9]+(?:\.[0-9]+)?|[0-9]+\.[0-9]{2}|class="[^"]*price[^"]*")', card_html)
    print("Found matches of interest in card block:")
    for m in matches[:20]:
        print(" -", m)
        
    # Let's search for the text "Cat Calming" to see its wrapper
    sub_idx = card_html.find("Cat Calming")
    while sub_idx != -1:
        print("\nOccurrence of Cat Calming text context:")
        print(card_html[sub_idx-100:sub_idx+300])
        sub_idx = card_html.find("Cat Calming", sub_idx+1)
else:
    print("Not found")
