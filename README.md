# Nutritional Profiles in USDA Foundation Foods

### Implications for Plant-Based Home Cooking

**Author:** Thomas Lu

**Date:** February 2026

---

## 🔬 Project Overview

This repository contains a comparative statistical analysis of 215 unique USDA Foundation Food items ( animal-based;  plant-based). The research investigates the physiological trade-offs of shifting to a plant-forward home-cooking environment, standardizing whole, unprocessed ingredients across gravimetric () and metabolic () scales.

## 📊 Key Findings

* **Protein Concentration:** Animal-based foods yield nearly  the median protein content of plant-based sources ( vs ).
* **Iron Density Paradox:** Per , plant-based foods exhibit a **10x higher median Iron density** than animal products ( vs ).
* **The B12 Gap:** Vitamin B12 is absent in  of plant-based samples, with presence restricted solely to fortified soy products.
* **Caloric Architecture:**  of animal-based calories are derived from protein and lipids, while plant-based calories are primarily carbohydrate-driven () and offer the exclusive pathway for dietary fiber.

## 🛠️ Tech Stack & Methodology

* **Language:** Python 3.x
* **Libraries:** `Pandas` (Data Processing), `Seaborn` & `Matplotlib` (Statistical Visualization).
* **Dataset:** USDA FoodData Central (Foundation Foods).
* **Metrics:** Standardized  units; calculated nutrient efficiency per .

## 📁 Repository Structure

```text
├── data/
│   ├── data.json              # Raw data from USDA
│   └── food_data.csv          # Cleaned data
├── output/                    
│   ├── summaries/             # CSV reports (Density, Macro Ratios, Correlation, etc.)
│   └── graphs/                # Generated visual analysis (Boxplots, Scatters, Bar Charts)
├── scripts/
│   ├── sort_data.py           # Data processing and cleaning logic
│   ├── plot_data.py           # Graph from cleaned data
│   └── summarize.py           # Generate statistical summaries from cleaned data
├── analysis_scripts.py        # Runs data processing and analysis scripts in order
├── requirements.txt           # Environment dependencies
└── README.md                  # Project documentation

```
## 🚀 Practical Implications

For the home cook, a transition to whole-food plant-based eating requires:

1. **Volumetric Adjustments:** Increasing plate volume to match traditional protein targets.
2. **Outlier Prioritization:** Focusing on high-protein plant sources (soy, legumes, nuts) to overcome lower protein-to-weight ratios.
3. **Intentional Supplementation:** Utilizing fortified foods or external supplements to address the absolute Vitamin B12 deficit in unprocessed plant ingredients.

## 📝 Data Availability

The original USDA raw files and full analysis code are available here. For a structured view of the metrics, see the [Project Spreadsheet](https://docs.google.com/spreadsheets/d/your-link-here).

