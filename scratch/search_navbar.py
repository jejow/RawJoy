with open(r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        if i > 500:
            break
        if 'cart' in line.lower() or 'checkout' in line.lower():
            if len(line.strip()) < 250:
                print(f"{i}: {line.strip()}")
            else:
                print(f"{i}: {line.strip()[:250]}...")
