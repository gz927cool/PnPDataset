import pandas as pd
import os

# Define paths
base_dir = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\07-Human-Merge"
mismatch_file = os.path.join(base_dir, "05-Potential_QID_Mismatches.csv")
corrected_file = os.path.join(base_dir, "06-Requery_Filled_Human_Merged_Corrected.csv")

print(f"Loading Mismatches from: {mismatch_file}")
df_mismatch = pd.read_csv(mismatch_file)

print(f"Loading Corrected Data from: {corrected_file}")
df_corrected = pd.read_csv(corrected_file)

# Group mismatches by QID to see which names were conflicting
mismatch_groups = df_mismatch.groupby('Original-QID')['Refined_Formal_Name'].apply(set).to_dict()

print("-" * 30)
print("Checking status of previously identified mismatches...")

resolved_count = 0
unresolved_count = 0
still_present_groups = []

for qid, bad_names in mismatch_groups.items():
    # Check what names are associated with this QID in the corrected file
    current_rows = df_corrected[df_corrected['Original-QID'] == qid]
    current_names = set(current_rows['Refined_Formal_Name'].unique())
    
    # If the QID is no longer in the dataset, it's "resolved" (or removed)
    if len(current_names) == 0:
        # print(f"QID {qid} (was {bad_names}) is no longer in the dataset.")
        resolved_count += 1
        continue

    # If the QID is present, check if it still has multiple names from the "bad" set
    # We care if the intersection of current names and bad names has > 1 element
    # OR if the current names for this QID are still multiple and suspicious
    
    # Actually, the simple check is: Does this QID still map to multiple distinct entities?
    # In the corrected file, we expect 1 QID -> 1 Entity (though maybe multiple name variations like "Homer" and "Homer (人物)")
    
    # Let's look at the intersection.
    # If 'Zeuxis' and 'Homer' were sharing Q11710021, and now only 'Homer' has it, that's good.
    
    remaining_bad_names = current_names.intersection(bad_names)
    
    if len(remaining_bad_names) > 1:
        # Still has multiple names from the original mismatch group
        print(f"[UNRESOLVED] QID {qid} still shared by: {remaining_bad_names}")
        unresolved_count += 1
        still_present_groups.append((qid, remaining_bad_names))
    else:
        # It might still have multiple names, but maybe they are valid variations (e.g. Homer, Homer (人物))
        # Let's check if any of the *other* names from the bad group are now associated with *different* QIDs
        
        # For each name in the original bad group, find its NEW QID
        # print(f"[RESOLVED] QID {qid} now only has: {current_names}")
        resolved_count += 1

print("-" * 30)
print(f"Total Mismatch Groups Checked: {len(mismatch_groups)}")
print(f"Resolved Groups: {resolved_count}")
print(f"Unresolved Groups: {unresolved_count}")

if unresolved_count == 0:
    print("\nGreat! All previously identified mismatches appear to be resolved (or reduced to single entities).")
else:
    print("\nSome mismatches persist. Please check the list above.")

# Also, let's specifically check the ones we fixed manually to confirm
print("-" * 30)
print("Verifying specific manual corrections:")
targets = ["Zeuxis", "Zechariah", "Teresa of Ávila", "Theresa of Avila (人物)", "Theseus"]
for name in targets:
    row = df_corrected[df_corrected['Refined_Formal_Name'] == name]
    if not row.empty:
        print(f"{name}: {row['Original-QID'].values[0]}")
    else:
        print(f"{name}: Not Found")
