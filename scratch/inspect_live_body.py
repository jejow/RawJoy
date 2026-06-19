import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"C:\Users\junxi\.gemini\antigravity-ide\brain\57f46918-4819-485d-a3dd-5d807b5ebcf7\.system_generated\steps\1916\content.md"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for idx in range(1000, len(lines)):
    print(f"Line {idx+1}: {lines[idx].strip()[:200]}")
