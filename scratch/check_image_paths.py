import os

slugMapping = {
  "beef-spinach-stew": "products/beef-spinach-stew/images/BeefSpinachStew-361.jpg",
  "cat-calming-formula": "products/cat-calming-formula/images/CatCalmingFormula-345.jpg",
  "cat-wellness-mix": "products/cat-wellness-mix/images/CatWellnessMix-341.jpg",
  "chicken-bone-treat": "products/chicken-bone-treat/images/ChickenBoneTreat-418.jpg",
  "chicken-herb-stick": "products/chicken-herb-stick/images/ChickenHerbStick-409.jpg",
  "chicken-pumpkin-pate": "products/chicken-pumpkin-pate/images/ChickenPumpkinPate-357.jpg",
  "crunchy-bone-treat": "products/crunchy-bone-treat/images/CrunchyBoneTreat-373.jpg",
  "doggy-dental-mix": "products/doggy-dental-mix/images/DailyNutritionMix-1.jpg",
  "duck-soft-chews": "products/duck-soft-chews/images/DuckSoftChews-353.jpg",
  "fish-bone-treat": "products/fish-bone-treat/images/FishBoneTreat-413.jpg",
  "juicy-turkey-crunch": "products/juicy-turkey-crunch/images/JuicyTurkeyCrunch-349.jpg",
  "juicy-turkey-stick": "products/juicy-turkey-stick/images/JuicyTurkeyStick-401.jpg",
  "lamb-quinoa-blend": "products/lamb-quinoa-blend/images/LambQuinoaBlend-393.jpg",
  "mackerel-salmon-kibble": "products/mackerel-salmon-kibble/images/MackerelSalmonKibble-381.jpg",
  "mint-comfort-bowl-series": "products/mint-comfort-bowl-series/images/MintComfortBowlSeries-431.jpg",
  "pastel-pet-bowl-series": "products/pastel-pet-bowl-series/images/PastelPetBowlSeries-427.jpg",
  "pet-meal-time-mix": "products/pet-meal-time-mix/images/PetMealTimeMix-337.jpg",
  "rawjoy-blue-energy-bar": "products/rawjoy-blue-energy-bar/images/RawJoyBlueEnergyBar-423.jpg",
  "rawjoy-green-bar": "products/rawjoy-green-bar/images/RawJoyGreenBar-377.jpg",
  "rawjoy-soft-bar": "products/rawjoy-soft-bar/images/RawJoySoftBar-369.jpg",
  "salmon-broccoli-crunch": "products/salmon-broccoli-crunch/images/SalmonBroccoliCrunch-385.jpg",
  "salmon-carrot-pate": "products/salmon-carrot-pate/images/SalmonCarrotPate-365.jpg",
  "salmon-rice-formula": "products/salmon-rice-formula/images/SalmonRiceFormula-389.jpg",
  "salmon-stick": "products/salmon-stick/images/SalmonStick-405.jpg",
  "venison-peas-recipe": "products/venison-peas-recipe/images/VenisonPeasRecipe-397.jpg"
}

print("Checking mapped paths:")
for slug, path in slugMapping.items():
    exists_as_mapped = os.path.exists(path)
    
    # Try looking in root images/ folder using the filename
    filename = os.path.basename(path)
    root_images_path = os.path.join("images", filename)
    exists_in_root_images = os.path.exists(root_images_path)
    
    print(f"{slug}:")
    print(f"  - Mapped path exists: {exists_as_mapped} ({path})")
    print(f"  - Root images path exists: {exists_in_root_images} ({root_images_path})")
