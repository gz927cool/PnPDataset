import pandas as pd
import os

# Define paths
base_dir = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\07-Human-Merge"
input_file = os.path.join(base_dir, "06-Requery_Filled_Human_Merged_Corrected.csv")
output_file = os.path.join(base_dir, "06-Requery_Filled_Human_Merged_Corrected.csv") # Overwrite

print(f"Reading {input_file}...")
df = pd.read_csv(input_file)

# Fix 1: Trim whitespace from QIDs
# This handles the 'Q110196230 ' case
df['Original-QID'] = df['Original-QID'].astype(str).str.strip()

# Fix 2: Replace '---' with empty string
df.loc[df['Original-QID'] == '---', 'Original-QID'] = ''

# Fix 3: Ensure 'nan' strings are actual NaNs (pandas read_csv usually handles this, but str conversion might revert it)
df.loc[df['Original-QID'].str.lower() == 'nan', 'Original-QID'] = ''

# Verify fixes
print("Verifying fixes...")
problem_1 = df[df['Refined_Formal_Name'] == 'Fondamenta Foscarini']
print(f"Fondamenta Foscarini QID: '{problem_1['Original-QID'].values[0]}'")

problem_2 = df[df['Refined_Formal_Name'] == "Third Colonnade for St. Peter's Square"]
print(f"Third Colonnade QID: '{problem_2['Original-QID'].values[0]}'")

# Save
df.to_csv(output_file, index=False)
print(f"Saved cleaned file to {output_file}")
