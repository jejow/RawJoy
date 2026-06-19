import re

with open('products/pastel-pet-bowl-series/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'(<script id="captcha-bootstrap">.*?</script>)', content, re.DOTALL)
if match:
    print("LENGTH:", len(match.group(1)))
    print(match.group(1))
else:
    print("Not found")
