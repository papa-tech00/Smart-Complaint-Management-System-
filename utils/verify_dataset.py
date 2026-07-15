import pandas as pd

df = pd.read_csv("data/complaints.csv")

print("Shape:", df.shape)
print()

print("Columns:")
print(df.columns)
print()

print("Category Counts:")
print(df["category"].value_counts())
print()

print("Missing Values:")
print(df.isnull().sum())
print()

print("Sample Data:")
print(df.sample(5))