import pandas as pd
import os

# Define paths
base_dir = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\07-Human-Merge"
input_file = os.path.join(base_dir, "03-Requery_Filled_Human_Merged_Cleaned.csv")
output_file = os.path.join(base_dir, "04-Requery_Filled_Human_Merged_Final.csv")

# Read the CSV
df = pd.read_csv(input_file)

print(f"Original Row Count: {len(df)}")

# Split into rows with QID and without QID
# We only deduplicate rows that HAVE a QID.
mask_has_qid = df['Original-QID'].notna() & (df['Original-QID'].str.strip() != '')
df_qid = df[mask_has_qid].copy()
df_no_qid = df[~mask_has_qid].copy()

print(f"Rows with QID: {len(df_qid)}")
print(f"Rows without QID: {len(df_no_qid)}")

# Helper columns for sorting priority
# Priority 1: Has Label (True is better)
df_qid['Has_Label'] = df_qid['Second-Query_Label'].notna() & (df_qid['Second-Query_Label'].str.strip() != '')

# Priority 2: Name does NOT contain "(人物)" (True is better)
df_qid['Clean_Name'] = ~df_qid['Refined_Formal_Name'].str.contains(r'\(人物\)', regex=True)

# Sort values to put the "best" rows at the top
# Ascending=False means True comes first
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

# Sort by Name for readability
df_final.sort_values(by='Refined_Formal_Name', inplace=True)

print(f"Final Row Count: {len(df_final)}")

# Save
df_final.to_csv(output_file, index=False)
print(f"Saved to {output_file}")
