import pandas as pd
from utils.data_loader import load_data, clean_data

print("--- DEBUG DATA ---")
df = load_data()
if df is None:
    print("Error loading data")
    exit()

print(f"Raw Shape: {df.shape}")
print(f"Raw Age unique: {df['Age'].unique()}")
print(f"Raw Card unique: {df['Card'].unique()}")

df_clean = clean_data(df)
print(f"Clean Shape: {df_clean.shape}")
print(f"Clean Age unique: {df_clean['Age'].unique()}")
print(f"Clean Age value_counts:\n{df_clean['Age'].value_counts(dropna=False)}")

print(f"Clean Card unique: {df_clean['Card'].unique()}")
print(f"Clean Card value_counts:\n{df_clean['Card'].value_counts(dropna=False)}")

print("--- END DEBUG ---")
