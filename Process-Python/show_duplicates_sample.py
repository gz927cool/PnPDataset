import pandas as pd
import os

# Define paths
base_dir = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\07-Human-Merge"
input_file = os.path.join(base_dir, "03-Requery_Filled_Human_Merged_Cleaned.csv")

# Read the CSV
df = pd.read_csv(input_file)

# Filter for rows with QID
mask_has_qid = df['Original-QID'].notna() & (df['Original-QID'].str.strip() != '')
df_qid = df[mask_has_qid].copy()

# Find duplicates based on QID
# keep=False marks all duplicates as True
duplicates = df_qid[df_qid.duplicated(subset=['Original-QID'], keep=False)]

# Sort by QID to group them together
duplicates_sorted = duplicates.sort_values(by='Original-QID')

print(f"Total duplicate rows found (sharing QID): {len(duplicates_sorted)}")
print("-" * 50)

# Show top 10 groups of duplicates
unique_duplicate_qids = duplicates_sorted['Original-QID'].unique()

for qid in unique_duplicate_qids[:10]:
    print(f"QID: {qid}")
    group = duplicates_sorted[duplicates_sorted['Original-QID'] == qid]
    # Select relevant columns to display
    print(group[['Refined_Formal_Name', 'Second-Query_Label']].to_string(index=False))
    print("-" * 50)
