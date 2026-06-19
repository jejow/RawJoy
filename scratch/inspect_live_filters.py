import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"C:\Users\junxi\.gemini\antigravity-ide\brain\57f46918-4819-485d-a3dd-5d807b5ebcf7\.system_generated\steps\1916\content.md"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

print(f"Content length: {len(content)}")
print("Does it contain 'password'?", "password" in content.lower())
print("Does it contain 'RawJoy'?", "rawjoy" in content.lower())

# Let's print lines 800 to 1000 to see what is on the page
lines = content.splitlines()
print(f"Total lines: {len(lines)}")
for idx in range(min(800, len(lines)), min(1000, len(lines))):
    print(f"{idx+1}: {lines[idx]}")
