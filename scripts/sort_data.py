import json
import pandas as pd
import re
from pathlib import Path

# setup directories and paths
current_dir = Path(__file__).parent
data_folder = current_dir.parent / "data"

input_path = data_folder / "data.json"
output_path = data_folder / "food_data.csv"

# Load JSON data
with open(input_path, "r") as f:
    data = json.load(f)

# Keywords for filtering
food_keywords = ["beans", "legumes", "tofu", "nuts", "vegetables", "meat", "eggs", "dairy", "fish"]  # customize
nutrient_keywords = ["protein", "fat", "carb", "fiber", "B-12", "calcium", "iron","energy"]

# Prepare list to store rows
rows = []

for food in data["FoundationFoods"]:
    food_name = food["description"]
    # Get foodCategory description if exists
    food_cat_desc = food.get("foodCategory", {}).get("description", "")

    # Check if any keyword matches the food description OR category description
    if any(keyword.lower() in food_name.lower() or keyword.lower() in food_cat_desc.lower() for keyword in food_keywords):
        row = {"Food": food_name, "FoodCategory": food_cat_desc}

        for nutrient in food["foodNutrients"]:
            nutrient_name = nutrient["nutrient"]["name"]
            # Check if any keyword matches the nutrient name

            if any(keyword.lower() in nutrient_name.lower() for keyword in nutrient_keywords):
                if "energy" in nutrient_name.lower():
                    nutrient_unit = nutrient["nutrient"]["unitName"]
                    row[str(nutrient_name + " " + nutrient_unit)] = nutrient.get("amount", None)
                else:
                    row[nutrient_name] = nutrient.get("amount", None)

        # Only add row if we found at least one nutrient
        if len(row) > 2:  # >2 because we now have Food and FoodCategory
            rows.append(row)

# Convert to DataFrame
df = pd.DataFrame(rows)

# Define mapping for concise column names
rename_map = {
    "Total lipid (fat)": "Fat",
    "Fatty acids, total saturated": "SaturatedFat",
    "Fatty acids, total monounsaturated": "MonounsaturatedFat",
    "Fatty acids, total polyunsaturated": "PolyunsaturatedFat",
    "Fatty acids, total trans": "TransFat",
    "Fatty acids, total trans-monoenoic": "TransMonoenoicFat",
    "Fatty acids, total trans-polyenoic": "TransPolyenoicFat",
    "Fatty acids, total trans-dienoic": "TransDienoicFat",
    "Total fat (NLEA)": "FatNLEA",
    "Carbohydrate, by difference": "CarbDiff",
    "Carbohydrate, by summation": "CarbSum",
    "Protein": "Protein",
    "Fiber, total dietary": "FiberL",
    "Total dietary fiber (AOAC 2011.25)": "Fiber",
    "Fiber, soluble": "SolubleFiber",
    "Fiber, insoluble": "InsolubleFiber",
    "Calcium, Ca": "Calcium",
    "Iron, Fe": "Iron",
    "Energy (Atwater General Factors) kcal": "EnergyGenFacKcal",
    "Energy (Atwater Specific Factors) kcal": "EnergySpeFacKcal",
    "Low Molecular Weight Dietary Fiber (LMWDF)": "LWMDFiber",
    "High Molecular Weight Dietary Fiber (HMWDF)": "HMWDFiber",
    "Vitamin B-12": "Vitamin B12"
}

# Rename columns
df = df.rename(columns=rename_map)

# Use AOAC fiber
df['Fiber'] = df['Fiber'].fillna(df['FiberL'])

# Use CarbDiff or CarbSum as the base (Total Carbs)
df['Carbs'] = df['CarbDiff'].fillna(df['CarbSum']).fillna(0).clip(lower=0)

# Fix USDA Data Gaps: Some items (like the 0% moisture beans) have Fiber recorded but are missing the Total Carbs value.
df['Carbs'] = df[['Carbs', 'Fiber']].max(axis=1)

# Compute Calories safely: kcal if exists, else kJ / 4.184
df['Calories'] = df['Energy kcal'].fillna(df['Energy kJ'] / 4.184).fillna(df['EnergyGenFacKcal']).fillna(df['EnergySpeFacKcal'])

# Compute calories by 4/4/9 when they fucked up
calculated_cals = (df['Protein'].fillna(0) * 4) + (df['Fat'].fillna(0) * 9) + (df['Carbs'].fillna(0) * 4)
df['Calories'] = df['Calories'].replace(0, pd.NA).fillna(calculated_cals).fillna(0)

# Keep only final columns
df = df[['Food', 'FoodCategory', 'Calories', 'Protein', 'Fat', 'Carbs', 'Fiber', 'Calcium', 'Iron', 'Vitamin B12']]

# Fill missing values with 0 just in case
df = df.fillna(0)

# Define mapping of categories to Plant vs Animal
plant_categories = [
    'Legumes and Legume Products',
    'Vegetables and Vegetable Products',
    'Nut and Seed Products'
]

animal_categories = [
    'Sausages and Luncheon Meats',
    'Dairy and Egg Products',
    'Poultry Products',
    'Finfish and Shellfish Products',
    'Beef Products',
    'Restaurant Foods'  # assume mostly animal-based
]

# Create a new column based on the mapping
def categorize_food(cat):
    if cat in plant_categories:
        return 'Plant-based'
    elif cat in animal_categories:
        return 'Animal-based'
    else:
        return 'Other'  # fallback for any uncategorized rows

df['FoodType'] = df['FoodCategory'].apply(categorize_food)

print(df.columns)

# Option 1: Save as CSV (human-readable)
df.to_csv(output_path, index=False)