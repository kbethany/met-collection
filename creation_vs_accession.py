import pandas as pd
import matplotlib.pyplot as plt

# Load and coerce to numeric, forcing errors to NaN
df = pd.read_csv("MetObjects.csv", usecols=["Object Begin Date", "AccessionYear"])
df["Object Begin Date"] = pd.to_numeric(df["Object Begin Date"], errors='coerce')
df["AccessionYear"] = pd.to_numeric(df["AccessionYear"], errors='coerce')

# Drop rows with NaN values
df = df.dropna(subset=["Object Begin Date", "AccessionYear"])

# Keep only plausible years (e.g., 0–2025)
df = df[
    (df["Object Begin Date"] > 0) &
    (df["Object Begin Date"] <= 2025) &
    (df["AccessionYear"] > 0) &
    (df["AccessionYear"] <= 2025)
]

# Plot the scatterplot
plt.figure(figsize=(10, 8))
plt.scatter(
    df["Object Begin Date"],
    df["AccessionYear"],
    alpha=0.03,
    s=1
)
plt.title("Object Creation Date vs. Accession Year")
plt.xlabel("Object Begin Date")
plt.ylabel("Accession Year")
plt.xlim(0, 2025)
plt.ylim(1875, 2025)
plt.grid(True)
plt.tight_layout()
plt.show()

# Save figure
plt.savefig("object-creation-date-vs-accession-date.png", dpi=300)

print("📊 Saved visualization as object-creation-date-vs-accession-date.png")

###Same as above but with dept
import seaborn as sns

df = pd.read_csv("MetObjects.csv", usecols=["Object Begin Date", "AccessionYear", "Department"])
df = df.dropna(subset=["Object Begin Date", "AccessionYear", "Department"])
df = df[(df["Object Begin Date"].astype(str).str.isnumeric()) & 
        (df["AccessionYear"].astype(str).str.isnumeric())]

df["Object Begin Date"] = df["Object Begin Date"].astype(int)
df["AccessionYear"] = df["AccessionYear"].astype(int)
df = df[(df["Object Begin Date"] > 0) & (df["AccessionYear"] <= 2025)]

# Sample 5000 rows for readability
df_sample = df.sample(n=5000, random_state=1)

plt.figure(figsize=(12, 8))
sns.scatterplot(data=df_sample, x="Object Begin Date", y="AccessionYear", hue="Department", alpha=0.7, s=20)
plt.title("Creation Year vs Accession Year Colored by Department")
plt.xlabel("Object Begin Date")
plt.ylabel("Accession Year")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', ncol=1)
plt.tight_layout()

# Save figure
plt.savefig("object-creation-date-vs-accession-date-with-dept.png", dpi=300)

print("📊 Saved visualization as object-creation-date-vs-accession-date-with-dept.png")

###What departments are most active and how their acquisitions change over time
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("MetObjects.csv", usecols=["Department", "AccessionYear"])
df = df.dropna(subset=["Department", "AccessionYear"])
df = df[df["AccessionYear"].apply(lambda x: str(x).isdigit())]
df["AccessionYear"] = df["AccessionYear"].astype(int)
df = df[df["AccessionYear"] <= 2025]  # Cap future years

# Group by year and department
grouped = df.groupby(["AccessionYear", "Department"]).size().unstack(fill_value=0)

# Plot
plt.figure(figsize=(14, 8))
grouped.rolling(window=5).mean().plot(ax=plt.gca(), linewidth=2)  # smooth a bit
plt.title("Acquisitions by Department Over Time")
plt.xlabel("Accession Year")
plt.ylabel("Number of Acquisitions")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Save figure
plt.savefig("acquisitions-by-dept-over-time.png", dpi=300)

print("📊 Saved visualization as acquisitions-by-dept-over-time.png")