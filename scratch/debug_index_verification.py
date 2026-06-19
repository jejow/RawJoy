import re
from bs4 import BeautifulSoup

filepath = "index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')

SALMON_STICK_ID = "9958927434018"
CAT_CALMING_ID = "9958900760866"

def is_target_element(el):
    pid = el.get('data-product-id')
    if pid in [SALMON_STICK_ID, CAT_CALMING_ID]:
        return pid
    text = str(el).lower()
    if 'salmon-stick' in text or 'salmon stick' in text:
        return SALMON_STICK_ID
    if 'cat-calming' in text or 'cat calming' in text:
        return CAT_CALMING_ID
    return None

for i, pp in enumerate(soup.find_all('product-price')):
    is_target = False
    if pp.get('data-product-id') in [SALMON_STICK_ID, CAT_CALMING_ID]:
        is_target = True
    else:
        card = pp.find_parent('product-card')
        if card:
            card_str = str(card).lower()
            if 'salmon-stick' in card_str or 'cat-calming' in card_str:
                is_target = True
        else:
            pp_str = str(pp).lower()
            if 'salmon-stick' in pp_str or 'cat-calming' in pp_str:
                is_target = True
                
    if is_target:
        container = pp.find(ref="priceContainer")
        compare_span = container.find(class_="compare-at-price") if container else None
        print(f"Index Product Price {i}:")
        print(f"  Container classes: {container.get('class') if container else None}")
        print(f"  Compare span content: '{compare_span.text if compare_span else None}'")
        card = pp.find_parent('product-card')
        if card:
            title = card.find(class_=re.compile(r'title')) or card.find('a', class_=re.compile(r'title'))
            print(f"  Parent Card Title: {title.text.strip() if title else 'Unknown'}")
        print("-" * 50)
