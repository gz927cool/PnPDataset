import pandas as pd
import os

# Define paths
base_dir = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\07-Human-Merge"
input_file = os.path.join(base_dir, "01-Requery_Filled_Human_Merged.csv")
output_file = os.path.join(base_dir, "02-Requery_Filled_Human_Merged_Deduplicated.csv")

# Read the CSV
df = pd.read_csv(input_file)

print(f"Original Row Count: {len(df)}")

# Deduplication Logic
# We want to keep the row that has a QID over one that doesn't.
# If both have QIDs, we keep the last one (assuming the appended Huma-Fillin rows are at the bottom and are more accurate).

# 1. Create a helper column to indicate if QID is present
df['Has_QID'] = df['Original-QID'].notna() & (df['Original-QID'].str.strip() != '')

# 2. Sort by Name and Has_QID (True > False)
# This ensures that for the same name, the one WITH a QID comes last (or first depending on sort).
# We want the "best" row to be last so we can use keep='last'.
df.sort_values(by=['Refined_Formal_Name', 'Has_QID'], ascending=[True, True], inplace=True)

# 3. Drop duplicates based on Name, keeping the last one (which should be the one with QID)
df_dedup = df.drop_duplicates(subset=['Refined_Formal_Name'], keep='last')

# Remove helper column
df_dedup = df_dedup.drop(columns=['Has_QID'])

print(f"Deduplicated Row Count: {len(df_dedup)}")
print(f"Removed {len(df) - len(df_dedup)} duplicate rows.")

# Save
df_dedup.to_csv(output_file, index=False)
print(f"Saved to {output_file}")
