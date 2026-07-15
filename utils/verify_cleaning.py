import pandas as pd

clean = pd.read_csv("data/complaints_clean.csv")

print("========== COLUMN NAMES ==========")
print(clean.columns)

print("\n========== FIRST 5 ROWS ==========")
print(clean.head())

print("\n========== MISSING VALUES ==========")
print(clean.isnull().sum())

print("\n========== DUPLICATES ==========")
print(clean.duplicated().sum())