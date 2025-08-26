import pandas as pd

# Check what columns are in the sample Excel
df = pd.read_excel('Prime_Enrollment_Sample.xlsx', sheet_name='Cleaned use this one', header=4)
print("Columns in sample Excel:")
print(df.columns.tolist())
print("\nFirst few rows:")
print(df.head())