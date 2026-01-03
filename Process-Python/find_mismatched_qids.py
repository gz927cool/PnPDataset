import pandas as pd
import os
from difflib import SequenceMatcher

# Define paths
base_dir = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\07-Human-Merge"
input_file = os.path.join(base_dir, "03-Requery_Filled_Human_Merged_Cleaned.csv")
output_file = os.path.join(base_dir, "05-Potential_QID_Mismatches.csv")

# Read the CSV
df = pd.read_csv(input_file)

# Filter for rows with QID
mask_has_qid = df['Original-QID'].notna() & (df['Original-QID'].str.strip() != '')
df_qid = df[mask_has_qid].copy()

# Group by QID
grouped = df_qid.groupby('Original-QID')

suspicious_groups = []

def is_similar(a, b):
    # Simple check: one contains the other
    if a in b or b in a:
        return True
    # Check similarity ratio
    return SequenceMatcher(None, a, b).ratio() > 0.6

print(f"Scanning {len(grouped)} QID groups for mismatches...")

for qid, group in grouped:
    unique_names = group['Refined_Formal_Name'].unique()
    
    if len(unique_names) > 1:
        # Check if names are significantly different
        # We compare the first name with others. If any pair is very different, we flag the group.
        # This is a heuristic.
        
        names = list(unique_names)
        is_suspicious = False
        
        # Compare all pairs
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                n1 = str(names[i]).lower()
                n2 = str(names[j]).lower()
                
                # Remove common suffixes for comparison
                n1_clean = n1.replace(' (人物)', '').replace(' (work)', '')
                n2_clean = n2.replace(' (人物)', '').replace(' (work)', '')
                
                if not is_similar(n1_clean, n2_clean):
                    is_suspicious = True
                    break
            if is_suspicious:
                break
        
        if is_suspicious:
            # Add all rows for this QID to the report
            for _, row in group.iterrows():
                suspicious_groups.append(row)

# Create DataFrame from suspicious rows
if suspicious_groups:
    result_df = pd.DataFrame(suspicious_groups)
    # Sort by QID for easy reading
    result_df.sort_values(by=['Original-QID', 'Refined_Formal_Name'], inplace=True)
    
    # Save
    result_df.to_csv(output_file, index=False)
    
    print(f"Found {len(result_df)} rows in suspicious groups.")
    print(f"Saved report to {output_file}")
    
    # Print a preview
    print("-" * 50)
    print("Preview of Potential Mismatches:")
    current_qid = None
    for _, row in result_df.head(20).iterrows():
        if row['Original-QID'] != current_qid:
            print("-" * 30)
            print(f"QID: {row['Original-QID']}")
            current_qid = row['Original-QID']
        print(f"  - {row['Refined_Formal_Name']} (Label: {row.get('Second-Query_Label', 'N/A')})")
else:
    print("No obvious mismatches found based on similarity threshold.")
