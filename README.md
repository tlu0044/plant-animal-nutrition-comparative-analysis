# Nutritional Profiles in USDA Foundation Foods

### Implications for Plant-Based Home Cooking

**Author:** Thomas Lu\
**Date:** February 2026

---

## Project Overview

This repository contains a comparative statistical analysis of 215 unique USDA Foundation Food items categorized into animal-based (n=80) and plant-based (n=135). The research investigates the physiological implications of shifting to a plant-based home-cooking environment, standardizing whole, unprocessed ingredients across gravimetric (100g) and metabolic (100kcal) scales.

## Key Findings

* **Protein Concentration:** Animal-based foods yield nearly 7x the median protein content of plant-based sources (16.60g vs 2.41g).
* **Iron Density Paradox:** Per 100kcal, plant-based foods exhibit a 10x higher median Iron density than animal products (1.18mg vs 0.11mg).
* **The B12 Gap:** Vitamin B12 is absent in 98.6% of plant-based samples, only in fortified soy products.
* **Caloric Architecture:** 90% of animal-based calories are derived from protein and lipids, while plant-based calories are primarily carbohydrate-driven (59%) are high in dietary fiber.

## Tech Stack & Methodology

* **Language:** Python 3.x
* **Libraries:** `Pandas` (Data Processing), `Seaborn` & `Matplotlib` (Statistical Visualization).
* **Dataset:** USDA FoodData Central (Foundation Foods).
* **Metrics:** Standardized 100g units; calculated nutrient efficiency per 100kcal.

## Repository Structure

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
## Practical Implications

For the home cook, a transition to whole-food plant-based eating requires:

1. **Volumetric Adjustments:** Increasing plate volume to match traditional protein targets.
2. **Outlier Prioritization:** Focusing on high-protein plant sources (soy, legumes, nuts) to overcome lower protein-to-weight ratios.
3. **Intentional Supplementation:** Utilizing fortified foods or external supplements to address the absolute Vitamin B12 deficit in unprocessed plant ingredients.

## Data Availability

The original USDA raw files and full analysis code are available here. For a structured view of the metrics, see the [Project Spreadsheet](https://docs.google.com/spreadsheets/d/1PYvKLAUffwFwzloVkGrtkIXmxZJn2mtFJ7IbtUHA4Hw/edit?usp=sharing).\
[Read the Full Research Report (PDF)](nutrition_analysis_report.pdf)

