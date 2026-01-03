import pandas as pd
import os

# Define paths
base_dir = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\07-Human-Merge"
# We go back to the Cleaned version (before QID deduplication) to rescue the rows that were dropped due to bad QIDs
input_file = os.path.join(base_dir, "03-Requery_Filled_Human_Merged_Cleaned.csv")
output_file = os.path.join(base_dir, "06-Requery_Filled_Human_Merged_Corrected.csv")

# Read the CSV
df = pd.read_csv(input_file)

# Apply Name Corrections first
name_changes = {
    "Theresa of Avila (人物)": "Teresa of Ávila"
}

for old_name, new_name in name_changes.items():
    mask = df['Refined_Formal_Name'] == old_name
    if mask.any():
        df.loc[mask, 'Refined_Formal_Name'] = new_name
        print(f"Renamed {mask.sum()} row(s) from '{old_name}' to '{new_name}'")

# Define corrections
corrections = {
    "Zeuxis": "Q197044",
    "Zechariah": "Q139464",
    "Teresa of Ávila": "Q174880",
    "Theseus": "Q1320718"
}

print("Applying corrections to 03-Cleaned file...")

updated_count = 0

for name, new_qid in corrections.items():
    # Find rows matching the name
    mask = df['Refined_Formal_Name'] == name
    
    if mask.any():
        # Update QID
        df.loc[mask, 'Original-QID'] = new_qid
        count = mask.sum()
        updated_count += count
        print(f"Updated {count} row(s) for '{name}' to QID {new_qid}")
    else:
        print(f"Name '{name}' not found in dataset.")

# Now that we've corrected the QIDs, these rows won't collide with their previous "twins" (like Homer).
# However, we should still run the deduplication logic again to ensure the dataset is clean.
# Logic from deduplicate_by_qid_priority.py:

print("Re-running deduplication logic...")

# Split into rows with QID and without QID
mask_has_qid = df['Original-QID'].notna() & (df['Original-QID'].str.strip() != '')
df_qid = df[mask_has_qid].copy()
df_no_qid = df[~mask_has_qid].copy()

# Helper columns for sorting priority
df_qid['Has_Label'] = df_qid['Second-Query_Label'].notna() & (df_qid['Second-Query_Label'].str.strip() != '')
df_qid['Clean_Name'] = ~df_qid['Refined_Formal_Name'].str.contains(r'\(人物\)', regex=True)

# Sort values
df_qid.sort_values(
    by=['Original-QID', 'Has_Label', 'Clean_Name'], 
    ascending=[True, False, False], 
    inplace=True
)

# Deduplicate keeping the first (best) one
df_qid_dedup = df_qid.drop_duplicates(subset=['Original-QID'], keep='first')

# Remove helper columns
df_qid_dedup = df_qid_dedup.drop(columns=['Has_Label', 'Clean_Name'])

print(f"Deduplicated QID Rows: {len(df_qid_dedup)}")
print(f"Removed {len(df_qid) - len(df_qid_dedup)} duplicates.")

# Combine back
df_final = pd.concat([df_qid_dedup, df_no_qid], ignore_index=True)
df_final.sort_values(by='Refined_Formal_Name', inplace=True)

# Save
df_final.to_csv(output_file, index=False)
print("-" * 30)
print(f"Total rows updated: {updated_count}")
print(f"Final row count: {len(df_final)}")
print(f"Saved corrected and deduplicated file to {output_file}")
