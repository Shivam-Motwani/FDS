import pandas as pd

# Load the new normalized dataset
df = pd.read_csv('Production_Crops_Livestock_E_All_Data_(Normalized)/Production_Crops_Livestock_E_All_Data_(Normalized).csv', 
                 encoding='latin1')

print(f"Shape: {df.shape}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nFirst few rows:")
print(df.head())
print(f"\nData types:")
print(df.dtypes)
print(f"\nUnique Areas: {df['Area'].nunique() if 'Area' in df.columns else 'N/A'}")
print(f"Unique Items: {df['Item'].nunique() if 'Item' in df.columns else 'N/A'}")
print(f"\nYear columns: {[col for col in df.columns if col.startswith('Y')]}")
