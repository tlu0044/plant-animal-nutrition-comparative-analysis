import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np


# Load the dataset
df = pd.read_csv('food_data.csv')

counts = df['FoodCategory'].value_counts()
print(counts)
