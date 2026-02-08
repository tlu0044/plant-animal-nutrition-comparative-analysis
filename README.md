# Comparative Nutritional Analysis: Plant-Based vs. Animal-Based Metabolic Profiles

## 🔬 Project Overview
This project provides a data-driven comparison of the nutritional compositions of animal-based and plant-based foods. Using a dataset of 200+ food items, the study investigates caloric efficiency, macronutrient distribution, and micronutrient density (specifically Iron, Calcium, and Vitamin B12).

The primary goal is to move beyond "per 100g" comparisons—which can be biased by water weight—and analyze **nutrient density per 100 kcal** to determine the metabolic efficiency of different dietary sources.

## 📊 Key Research Findings
* **The Iron Density Paradox:** While animal products have higher absolute protein, plant-based foods in this dataset show a **median Iron density 10x higher** than animal products when normalized per 100 kcal ($1.18mg$ vs $0.11mg$).
* **Protein Efficiency:** Animal-based foods remain the most calorie-efficient protein sources, with a median of $8.78g$ of protein per 100 kcal, compared to $5.11g$ in plant-based sources.
* **The B12 Gap:** Vitamin B12 presence is a binary divider; $58.7\%$ of animal products contain B12, whereas only $1.4\%$ of plant products (fortified milks) provide the nutrient.
* **Caloric Identity:** Animal-based calories are split almost equally between Protein ($46\%$) and Fat ($44\%$), whereas plant-based calories are dominated by Carbohydrates ($59\%$).

## 🛠️ Tech Stack & Methodology
* **Language:** Python 3.x
* **Libraries:** `Pandas` (Data Engineering), `Matplotlib/Seaborn` (Statistical Visualization), `Numpy` (Vectorized Math).
* **Data Normalization:** Created a "Safe Calorie" pipeline to calculate nutrient-to-calorie ratios without division-by-zero errors for low-calorie items.
* **Statistical Tools:** Correlation Heatmaps, Box-and-Whisker Distributions, and Powerhouse Ranking algorithms.

## 📂 Repository Structure
```text
├── data/
│   └── food_data.csv          # Raw nutritional data
├── graphs/                    # Generated visual analysis (Boxplots, Scatters)
├── summaries/                 # CSV reports (Density, Macro Ratios, Top Foods)
├── analysis_scripts.py        # Core data processing & plotting logic
├── requirements.txt           # Environment dependencies
└── README.md                  # Project documentation