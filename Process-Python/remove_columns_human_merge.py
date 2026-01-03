import pandas as pd
import os

# Define paths
base_dir = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\07-Human-Merge"
input_file = os.path.join(base_dir, "02-Requery_Filled_Human_Merged_Deduplicated.csv")
output_file = os.path.join(base_dir, "03-Requery_Filled_Human_Merged_Cleaned.csv")

# Read the CSV
df = pd.read_csv(input_file)

# Columns to remove
cols_to_remove = ['Second-Query_QID', 'LLM-Fillin_QID']

# Drop columns if they exist
df.drop(columns=[c for c in cols_to_remove if c in df.columns], inplace=True)

# Save
df.to_csv(output_file, index=False)
print(f"Processed file saved to: {output_file}")
print(f"Removed columns: {cols_to_remove}")
print(f"Remaining columns: {df.columns.tolist()}")
