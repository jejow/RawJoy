import sys

def search_in_file(filepath, query):
    print(f"Searching for '{query}' in {filepath}:")
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            if query.lower() in line.lower():
                print(f"Line {i}: {line.strip()[:150]}")

if __name__ == "__main__":
    filepath = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\index.html"
    query = sys.argv[1] if len(sys.argv) > 1 else "cart"
    search_in_file(filepath, query)
