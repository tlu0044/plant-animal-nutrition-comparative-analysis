import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def main():
    # setup directories and paths
    current_dir = Path(__file__).parent
    input_path = current_dir.parent / "data" / "food_data.csv"
    output_path = current_dir.parent / "output" / "graphs"

    # make folders if they dont exist
    output_path.mkdir(parents=True, exist_ok=True)

    # load data
    df = pd.read_csv(input_path)

    # christmas colors
    sns.set_theme(style="whitegrid")
    custom_palette = {'Plant-based': '#2ecc71', 'Animal-based': '#e74c3c', 'Other': '#95a5a6'}

    # distribution box plots for each nutrient
    nutrients = ['Protein', 'Fat', 'Carbs', 'Fiber', 'Calories', 'Vitamin B12','Calcium','Iron']
    for nutrient in nutrients:
        plt.figure(figsize=(8, 6))
        sns.boxplot(x='FoodType', y=nutrient, data=df, hue='FoodType', palette=custom_palette, legend=False)
        if nutrient == "Calories":
            unit = "kcal"
        elif nutrient == "Vitamin B12":
            unit = "mcg"
        elif nutrient == "Calcium" or nutrient == "Iron":
            unit = "mg"
        else:
            unit = "g"
        plt.title(f'Distribution of {nutrient} per 100g')
        plt.ylabel(f'{nutrient} ({unit})')
        plt.tight_layout()
        plt.savefig(output_path/f'boxplot_{nutrient.lower().replace(" ", "_")}.png')
        plt.close()

    # scatter plot for protein vs calories
    plt.figure(figsize=(10, 7))
    sns.scatterplot(data=df, x='Calories', y='Protein', hue='FoodType', 
                    palette=custom_palette, s=100, alpha=0.7)
    plt.title('Protein Density: Protein vs Calories')
    plt.xlabel('Calories (kcal/100g)')
    plt.ylabel('Protein (g/100g)')
    plt.tight_layout()
    plt.savefig(output_path/'scatter_protein_density.png')
    plt.close()

    # scatter plot for carbs vs fiber
    plt.figure(figsize=(10, 7))
    sns.scatterplot(data=df, x='Carbs', y='Fiber', hue='FoodType', 
                    palette=custom_palette, s=100, alpha=0.7)
    plt.title('Carbohydrate Quality: Fiber vs Total Carbs')
    plt.xlabel('Total Carbohydrates (g/100g)')
    plt.ylabel('Fiber (g/100g)')
    plt.tight_layout()
    plt.savefig(output_path/'scatter_carb_quality.png')
    plt.close()

    # macro avg bar chart
    avg_data = df.groupby('FoodType')[['Protein', 'Fat', 'Carbs', 'Fiber', 'Calcium', 'Iron']].mean().reset_index()
    macros_g = ['Protein', 'Fat', 'Carbs', 'Fiber']
    avg_macros = avg_data.melt(id_vars='FoodType', value_vars=macros_g, var_name='Nutrient', value_name='Average (g)')

    plt.figure(figsize=(10, 6))
    sns.barplot(data=avg_macros, x='Nutrient', y='Average (g)', hue='FoodType', palette=custom_palette)
    plt.title('Average Macronutrient Profile (g per 100g)')
    plt.ylabel('Weight (g)')
    plt.tight_layout()
    plt.savefig(output_path/'bar_avg_macros.png')
    plt.close()

    # micro avg bar chart
    avg_data = df.groupby('FoodType')[['Protein', 'Fat', 'Carbs', 'Fiber', 'Calcium', 'Iron', 'Vitamin B12']].mean().reset_index()

    # calcium and iron in mg
    micros_mg = ['Calcium', 'Iron']
    avg_micros = avg_data.melt(id_vars='FoodType', value_vars=micros_mg, var_name='Nutrient', value_name='Average (mg)')
    plt.figure(figsize=(8, 6))
    sns.barplot(data=avg_micros, x='Nutrient', y='Average (mg)', hue='FoodType', palette=custom_palette)
    plt.title('Average Micronutrient Profile (mg per 100g)')
    plt.ylabel('Weight (mg)')
    plt.tight_layout()
    plt.savefig(output_path/'bar_avg_micros.png')
    plt.close()

    # b12 in microg
    avg_b12 = avg_data.melt(id_vars='FoodType', value_vars=['Vitamin B12'], var_name='Nutrient', value_name='Average (mcg)')
    plt.figure(figsize=(8, 6))
    sns.barplot(data=avg_b12, x='Nutrient', y='Average (mcg)', hue='FoodType', palette=custom_palette)
    plt.title('Average Vitamin B12 Profile (mcg per 100g)')
    plt.ylabel('Weight (mcg)')
    plt.tight_layout()
    plt.savefig(output_path/'bar_avg_b12.png')
    plt.close()

    print("All graphs have been generated.")

if __name__ == "__main__":
    main()