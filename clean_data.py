# clean_data.py

import pandas as pd

# Load raw data
df = pd.read_csv("MetObjects.csv", low_memory=False)

# Keep only relevant columns
cols = [
    "Department", "AccessionYear", "Artist Display Name",
    "Artist Begin Date", "Artist End Date", "Artist Gender",
    "Object Begin Date", "Object End Date", "Medium", "Classification"
]
df = df[cols]

# Drop rows where Department or Classification is missing
df = df.dropna(subset=["Department", "Classification"])

# Fill missing ArtistGender with 'Unknown'
df["Artist Gender"] = df["Artist Gender"].fillna("Unknown")

# Normalize pipe-separated values in Classification (keep original too)
df["ClassificationList"] = df["Classification"].str.split("|")

# Convert dates to numeric (errors='coerce' turns bad entries into NaN)
date_cols = ["AccessionYear", "Artist Begin Date", "Artist End Date", "Object Begin Date", "Object End Date"]
df[date_cols] = df[date_cols].apply(pd.to_numeric, errors='coerce')

# Export cleaned dataset
df.to_csv("MetObjects_cleaned.csv", index=False)

print("✅ Cleaned dataset saved as MetObjects_cleaned.csv")
