import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("MetObjects.csv", usecols=[
    "Object Begin Date", "Classification"
])
df = df.dropna(subset=["Object Begin Date", "Classification"])

# Remove problematic dates
df = df[df["Object Begin Date"] > 0]

# Split Classification on '|'
df["Classification"] = df["Classification"].astype(str).str.split("|")

# Explode rows for multiple classifications
df = df.explode("Classification")
df["Classification"] = df["Classification"].str.strip()

# Group and count
grouped = df.groupby(["Object Begin Date", "Classification"]).size().reset_index(name="Count")

# Get top 10 classifications overall
top_classes = (
    grouped.groupby("Classification")["Count"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .index
)

# Filter for just those top 10
filtered = grouped[grouped["Classification"].isin(top_classes)]

# Pivot for plotting
pivot = filtered.pivot(index="Object Begin Date", columns="Classification", values="Count").fillna(0)

# Plot
pivot.rolling(window=5).mean().plot(figsize=(14, 8), lw=2)
plt.title("Top 10 Object Classifications Over Time (5-year rolling average)")
plt.ylabel("Number of Artworks")
plt.xlabel("Object Begin Date")
plt.grid(True)
plt.tight_layout()
plt.show()
