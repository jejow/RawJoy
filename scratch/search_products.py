filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Search for beef-spinach or calming
pats = ['beef-spinach', 'cat-calming', 'cat-wellness', 'chicken-bone', 'Rp', 'id-ID', '$']
for pat in pats:
    count = content.count(pat)
    print(f"Pattern '{pat}': count = {count}")
    if count > 0:
        # Print a snippet of first occurrence
        idx = content.find(pat)
        print(f"  Snippet: {content[max(0, idx-50):min(len(content), idx+100)]}")
