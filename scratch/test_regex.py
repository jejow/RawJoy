import re

with open('js/theme.js', 'r', encoding='utf-8') as f:
    line1 = f.readline()

print("Line 1 length:", len(line1))
# Let's find matches
matches = re.findall(r'import\s*.*?\s*from\s*["\'](.*?)["\']', line1)
print("Matches with .*?:", matches)

# A more specific non-space regex
matches_better = re.findall(r'import\s*\{?[^}]*\}?\s*from\s*["\']([^"\']+)["\']', line1)
print("Matches with better regex:", matches_better)
