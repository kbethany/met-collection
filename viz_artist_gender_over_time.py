import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV (reuse your filtered dataset if you want, or the full one)
df = pd.read_csv("MetObjects.csv", usecols=["Artist Gender", "Object Begin Date"])

# Filter out rows where Artist Gender or Object Begin Date is missing or invalid
df = df.dropna(subset=["Artist Gender", "Object Begin Date"])
df = df[df["Object Begin Date"] > 0]  # Remove non-positive years

print(df["Artist Gender"].value_counts(dropna=False))

# Show unique values in 'Artist Gender' column before grouping
print(df["Artist Gender"].unique())

print(gender_counts.sum(axis=0))

# Sometimes "Artist Gender" can have multiple values separated by '|'
# Clean the Artist Gender column
# Clean the Artist Gender column, allowing multiple genders separated by '|'
def clean_multiple_genders(gender_str):
    if pd.isna(gender_str) or gender_str.strip() == "":
        return "Unknown"
    
    genders = gender_str.split("|")
    cleaned = []
    
    for g in genders:
        g_clean = g.strip().lower()
        if g_clean in ["male", "m"]:
            cleaned.append("Male")
        elif g_clean in ["female", "f"]:
            cleaned.append("Female")
        elif g_clean in ["non-binary", "nonbinary", "nb"]:
            cleaned.append("Non-Binary")
        elif g_clean in ["transgender", "trans"]:
            cleaned.append("Transgender")
        elif g_clean in ["genderqueer"]:
            cleaned.append("Genderqueer")
        elif g_clean == "":
            cleaned.append("Unknown")
        else:
            cleaned.append(g_clean.capitalize())
    
    # Remove duplicates and sort
    cleaned_unique = sorted(set(cleaned))
    return "|".join(cleaned_unique)

df["Artist Gender"] = df["Artist Gender"].apply(clean_multiple_genders)

# Now group by year and each gender (split multi-gender values to count separately)
# Explode the multi-gender entries into multiple rows for counting
df_exploded = df.assign(**{
    "Artist Gender": df["Artist Gender"].str.split("|")
}).explode("Artist Gender")

# Group by year and gender, then count
gender_counts = df_exploded.groupby(["Object Begin Date", "Artist Gender"]).size().unstack(fill_value=0)

# Sort by year
gender_counts = gender_counts.sort_index()

# Create a continuous range of years for the x-axis
years = range(gender_counts.index.min(), gender_counts.index.max() + 1)

# Reindex to include all years, fill missing with 0
gender_counts = gender_counts.reindex(years, fill_value=0)

import matplotlib.pyplot as plt

plt.figure(figsize=(14, 7))

# stacked area plot
gender_counts.plot.area()

plt.title("Artworks by Artist Gender Over Time")
plt.xlabel("Object Begin Date (Year)")
plt.ylabel("Number of Artworks")
plt.legend(title="Artist Gender")
plt.grid(True, axis='y', alpha=0.3)

plt.show()
