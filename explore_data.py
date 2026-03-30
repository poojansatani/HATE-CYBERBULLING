import pandas as pd

# Dataset load karo
df = pd.read_csv('labeled_data.csv')

# Basic info juo
print("=== Dataset Shape ===")
print(df.shape)

print("\n=== Columns ===")
print(df.columns.tolist())

print("\n=== Pehla 5 rows ===")
print(df.head())

print("\n=== Class distribution ===")
print(df['class'].value_counts())