import json
import pandas as pd
from pathlib import Path

def main():
    # setup directories and paths
    current_dir = Path(__file__).parent
    input_path = current_dir.parent / "data" / "data.json"
    output_path = current_dir.parent / "data" / "food_data.csv"

    # load json data
    with open(input_path, "r") as f:
        data = json.load(f)

    # filtering words
    food_keywords = ["beans", "legumes", "tofu", "nuts", "vegetables", "meat", "eggs", "dairy", "fish"]  # customize
    nutrient_keywords = ["protein", "fat", "carb", "fiber", "B-12", "calcium", "iron","energy"]

    # store rows with matches
    rows = []

    for food in data["FoundationFoods"]:
        # get food name and category
        food_name = food["description"]
        food_cat_desc = food.get("foodCategory", {}).get("description", "")

        # check for keyword matches in name or description
        if any(keyword.lower() in food_name.lower() or keyword.lower() in food_cat_desc.lower() for keyword in food_keywords):
            row = {"Food": food_name, "FoodCategory": food_cat_desc}

            for nutrient in food["foodNutrients"]:
                nutrient_name = nutrient["nutrient"]["name"]
                # check nutrient keyword matches

                if any(keyword.lower() in nutrient_name.lower() for keyword in nutrient_keywords):
                    # grab unit if nutrient is energy (kcal/kJ)
                    if "energy" in nutrient_name.lower():
                        nutrient_unit = nutrient["nutrient"]["unitName"]
                        row[str(nutrient_name + " " + nutrient_unit)] = nutrient.get("amount", None)
                    else:
                        row[nutrient_name] = nutrient.get("amount", None)

            # add row when any nutrient is found (+name and category)
            if len(row) > 2:
                rows.append(row)

    # dataframe! (i hate them)
    df = pd.DataFrame(rows)

    # column names rename for eaasier management
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

    df = df.rename(columns=rename_map)

    # use aoac fiber and total fiber if no exist
    df['Fiber'] = df['Fiber'].fillna(df['FiberL'])

    # carbdiff or carbsum for total carbs
    df['Carbs'] = df['CarbDiff'].fillna(df['CarbSum']).fillna(0).clip(lower=0)

    # fix usda fuckups (when fiber > carbs)
    df['Carbs'] = df[['Carbs', 'Fiber']].max(axis=1)

    # calories conversion if only kJ exist
    df['Calories'] = df['Energy kcal'].fillna(df['Energy kJ'] / 4.184).fillna(df['EnergyGenFacKcal']).fillna(df['EnergySpeFacKcal'])

    # calculate calories by 4/4/9 because usda fucked up
    calculated_cals = (df['Protein'].fillna(0) * 4) + (df['Fat'].fillna(0) * 9) + (df['Carbs'].fillna(0) * 4)
    df['Calories'] = df['Calories'].replace(0, pd.NA).fillna(calculated_cals).fillna(0)

    # keep final columns
    df = df[['Food', 'FoodCategory', 'Calories', 'Protein', 'Fat', 'Carbs', 'Fiber', 'Calcium', 'Iron', 'Vitamin B12']]

    # make missing values with 0 just in case
    df = df.fillna(0)

    # mapping from category -> plant-based/animal-based
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

    # new column based on the mapping
    def categorize_food(cat):
        if cat in plant_categories:
            return 'Plant-based'
        elif cat in animal_categories:
            return 'Animal-based'
        else:
            return 'Other'  # hopefully doesnt happen

    df['FoodType'] = df['FoodCategory'].apply(categorize_food)

    # check
    #print(df.columns)

    # save to csv
    df.to_csv(output_path, index=False)

    print("Data has been successfully sorted and saved as csv.")

if __name__ == "__main__":
    main()