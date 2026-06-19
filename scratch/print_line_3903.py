with open(r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        if i == 3903:
            s = line.strip()
            print("LINE:", s)
            for idx, c in enumerate(s):
                print(f"{idx}: {repr(c)}")
            break

