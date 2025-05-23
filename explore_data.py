# explore_data.py

import pandas as pd

# Load the dataset
df = pd.read_csv("MetObjects.csv", low_memory=False)

# Shape of the data (rows, columns)
print("Shape of the dataset:", df.shape)

# Column names
print("\nColumn names:")
print(df.columns.tolist())

# First few rows
print("\nSample rows:")
print(df.head())

# Summary of each column
print("\nInfo:")
print(df.info())

# Count of missing values
print("\nMissing values (top 15):")
print(df.isnull().sum().sort_values(ascending=False).head(15))
