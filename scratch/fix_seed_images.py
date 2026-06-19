"""
Fix seed-data.json to use correct product-specific images as mainImage,
and also update the images array to include the correct product image first.
"""
import json
import os

# Correct product image mapping (slug -> correct product image file)
PRODUCT_IMAGES = {
    "beef-spinach-stew": "BeefSpinachStew-361.jpg",
    "cat-calming-formula": "CatCalmingFormula-345.jpg",
    "cat-wellness-mix": "CatWellnessMix-341.jpg",
    "chicken-bone-treat": "ChickenBoneTreat-418.jpg",
    "chicken-herb-stick": "ChickenHerbStick-409.jpg",
    "chicken-pumpkin-pate": "ChickenPumpkinPate-357.jpg",
    "crunchy-bone-treat": "CrunchyBoneTreat-373.jpg",
    "doggy-dental-mix": "DailyNutritionMix-1.jpg",
    "duck-soft-chews": "DuckSoftChews-353.jpg",
    "fish-bone-treat": "FishBoneTreat-413.jpg",
    "juicy-turkey-crunch": "JuicyTurkeyCrunch-349.jpg",
    "juicy-turkey-stick": "JuicyTurkeyStick-401.jpg",
    "lamb-quinoa-blend": "LambQuinoaBlend-393.jpg",
    "mackerel-salmon-kibble": "MackerelSalmonKibble-381.jpg",
    "mint-comfort-bowl-series": "MintComfortBowlSeries-431.jpg",
    "pastel-pet-bowl-series": "PastelPetBowlSeries-427.jpg",
    "pet-meal-time-mix": "PetMealTimeMix-337.jpg",
    "rawjoy-blue-energy-bar": "RawJoyBlueEnergyBar-423.jpg",
    "rawjoy-green-bar": "RawJoyGreenBar-377.jpg",
    "rawjoy-soft-bar": "RawJoySoftBar-369.jpg",
    "salmon-broccoli-crunch": "SalmonBroccoliCrunch-385.jpg",
    "salmon-carrot-pate": "SalmonCarrotPate-365.jpg",
    "salmon-rice-formula": "SalmonRiceFormula-389.jpg",
    "salmon-stick": "SalmonStick-405.jpg",
    "venison-peas-recipe": "VenisonPeasRecipe-397.jpg",
}

def fix_seed_data():
    seed_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'firebase', 'seed-data.json')
    
    with open(seed_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    products = data.get('products', [])
    fixed_count = 0
    
    for product in products:
        slug = product.get('slug', '')
        if slug in PRODUCT_IMAGES:
            correct_img = f"products/{slug}/images/{PRODUCT_IMAGES[slug]}"
            old_main = product.get('mainImage', '')
            
            if old_main != correct_img:
                product['mainImage'] = correct_img
                
                # Also update images array to include the product image as the first entry
                images = product.get('images', [])
                if correct_img not in images:
                    images.insert(0, correct_img)
                    product['images'] = images
                
                fixed_count += 1
                print(f"  Fixed {slug}: {old_main} -> {correct_img}")
            else:
                print(f"  OK    {slug}: already correct")
    
    with open(seed_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nFixed {fixed_count} product mainImage entries in seed-data.json")

if __name__ == '__main__':
    fix_seed_data()
