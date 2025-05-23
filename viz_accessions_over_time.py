# viz_accessions_over_time.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Style
sns.set(style="whitegrid")

# Load cleaned data
df = pd.read_csv("MetObjects_cleaned.csv")

# Keep only year and classification
df = df[["AccessionYear", "ClassificationList"]].dropna()

# Convert Classification List string to list
df["ClassificationList"] = df["ClassificationList"].str.strip("[]").str.replace("'", "").str.split(",")

# Explode to count each classification separately
df_exploded = df.explode("ClassificationList")
df_exploded["ClassificationList"] = df_exploded["ClassificationList"].str.strip()

# Count by year and classification
grouped = df_exploded.groupby(["AccessionYear", "ClassificationList"]).size().reset_index(name="Count")

# Pivot for stacked area
pivot = grouped.pivot(index="AccessionYear", columns="ClassificationList", values="Count").fillna(0)

# Only keep years after 1900
pivot = pivot[pivot.index >= 1900]

# Keep top 5 classifications only
top_classes = pivot.sum().sort_values(ascending=False).head(5).index
pivot_top = pivot[top_classes]

# Plot
plt.figure(figsize=(12, 6))
# Normalize each row to sum to 1 (percent composition)
pivot_top_percent = pivot_top.div(pivot_top.sum(axis=1), axis=0)

pivot_top_percent.plot.area(stacked=True, colormap="viridis", figsize=(12, 6))
plt.ylabel("Proportion of Acquisitions")

plt.title("Top 5 Classifications Acquired by Year", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Number of Items Acquired")
plt.tight_layout()

# Save
plt.savefig("accessions_over_time.png", dpi=300)
print("📈 Saved visualization as accessions_over_time.png")
