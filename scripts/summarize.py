import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def main():
    # setup directories and paths
    current_dir = Path(__file__).parent
    input_path = current_dir.parent / "data" / "food_data.csv"
    output_path = current_dir.parent / "output" / "summaries"

    # make folders if they dont exist
    output_path.mkdir(parents=True, exist_ok=True)

    # oad the data
    df = pd.read_csv(input_path)

    # descriptive statistics
    desc_stats = df.groupby('FoodType')[['Protein', 'Fat', 'Carbs', 'Fiber', 'Calories', 'Calcium', 'Iron', 'Vitamin B12']].describe().T
    desc_stats.to_csv(output_path/'descriptive_statistics.csv')

    # nutrient density per 100 kcal
    density_df = df.copy()
    density_df['Calories_Safe'] = density_df['Calories'].replace(0, np.nan)
    for nut, unit in [('Protein', 'g'), ('Iron', 'mg'), ('Calcium', 'mg'), ('Vitamin B12', 'mcg')]:
        density_df[f'{nut}_per_100kcal'] = (density_df[nut] / density_df['Calories_Safe']) * 100

    density_cols = [c for c in density_df.columns if 'per_100kcal' in c]
    density_summary = density_df.groupby('FoodType')[density_cols].agg(['mean', 'median'])
    density_summary.to_csv(output_path/'nutrient_density_per_100kcal.csv')

    # top foods
    ranking_list = []
    for nut in ['Protein', 'Iron', 'Calcium', 'Vitamin B12']:
        top = df.sort_values(['FoodType', nut], ascending=[True, False]).groupby('FoodType').head(5)
        ranking_list.append(top[['FoodType', 'Food', nut]])

    powerhouses = pd.concat(ranking_list, keys=['Top Protein', 'Top Iron', 'Top Calcium', 'Top B12'])
    powerhouses.to_csv(output_path/'powerhouse_foods.csv')

    # macro ratio to calories
    ratio_df = df.copy()
    ratio_df['Calories_Safe'] = ratio_df['Calories'].replace(0, np.nan)

    ratio_df['Protein_Pct_Cal'] = (ratio_df['Protein'] * 4 / ratio_df['Calories_Safe']) * 100
    ratio_df['Fat_Pct_Cal'] = (ratio_df['Fat'] * 9 / ratio_df['Calories_Safe']) * 100
    ratio_df['Carbs_Pct_Cal'] = (ratio_df['Carbs'] * 4 / ratio_df['Calories_Safe']) * 100

    macro_ratios = ratio_df.groupby('FoodType')[['Protein_Pct_Cal', 'Fat_Pct_Cal', 'Carbs_Pct_Cal']].mean().reset_index()
    macro_ratios.to_csv(output_path/'average_macro_calorie_ratios.csv')

    # b12 presence (% of food with b12 > 0)
    presence = df.groupby('FoodType')['Vitamin B12'].apply(lambda x: (x > 0).mean() * 100).reset_index()
    presence.columns = ['FoodType', 'B12 Presence Rate (%)']
    presence.to_csv(output_path/'b12_presence_rate.csv', index=False)

    # correlation map
    plt.figure(figsize=(10, 8))
    corr = df[['Protein', 'Fat', 'Carbs', 'Fiber', 'Calories', 'Calcium', 'Iron', 'Vitamin B12']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('Nutrient Correlation Heatmap')
    plt.tight_layout()
    plt.savefig(output_path/'correlation_heatmap.png')
    plt.close()

    print("All statistical summaries have been generated.")

if __name__ == "__main__":
    main()