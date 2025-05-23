# viz_top_classifications.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Use nice visual style
sns.set(style="whitegrid")

# Load cleaned data
df = pd.read_csv("MetObjects_cleaned.csv")

# Convert stringified list back to Python list
df["ClassificationList"] = df["ClassificationList"].str.strip("[]").str.replace("'", "").str.split(",")

# Explode list into rows
df_exploded = df.explode("ClassificationList")

# Strip whitespace
df_exploded["ClassificationList"] = df_exploded["ClassificationList"].str.strip()

# Count top classifications
top_class = df_exploded["ClassificationList"].value_counts().head(10)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(x=top_class.values, y=top_class.index, palette="viridis")
plt.title("Top 10 Classifications in The Met Collection", fontsize=14)
plt.xlabel("Number of Items")
plt.ylabel("Classification")
plt.tight_layout()

# Save figure
plt.savefig("top_classifications.png", dpi=300)

print("📊 Saved visualization as top_classifications.png")
