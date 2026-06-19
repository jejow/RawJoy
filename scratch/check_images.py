import re

def main():
    content = open('products/salmon-stick/index.html', encoding='utf-8').read()
    
    print("--- MAIN PRODUCT IMG TAGS ---")
    # Search for img tags in the main content area
    img_matches = re.findall(r'<img[^>]+>', content)
    for img in img_matches:
        if 'product__media' in img or 'media__image' in img or 'files/' in img:
            print(img)

if __name__ == '__main__':
    main()
