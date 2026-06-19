import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

collections_dir = r"c:\Users\junxi\OneDrive\Documents\SEMESTER 4\Pemrograman Web\RawJoy\collections"

p1_img_dir = os.path.join(collections_dir, "puppy-food", "images")
p2_img_dir = os.path.join(collections_dir, "puppy-food-1", "images")

p1_files = set(os.listdir(p1_img_dir)) if os.path.exists(p1_img_dir) else set()
p2_files = set(os.listdir(p2_img_dir)) if os.path.exists(p2_img_dir) else set()

print(f"puppy-food/images contains {len(p1_files)} files")
print(f"puppy-food-1/images contains {len(p2_files)} files")

print(f"\nFiles in puppy-food but not in puppy-food-1: {len(p1_files - p2_files)}")
print(f"Files in puppy-food-1 but not in puppy-food: {len(p2_files - p1_files)}")

# Check some specific files
for name in ["SalmonStick-405.jpg", "BeefSpinachStew-361.jpg", "DailyNutritionMix-1.jpg"]:
    print(f"\nChecking file: {name}")
    print(f"  - In puppy-food/images: {name in p1_files}")
    print(f"  - In puppy-food-1/images: {name in p2_files}")
