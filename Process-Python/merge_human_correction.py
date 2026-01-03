import csv
import os
import shutil

# Define paths
base_dir = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin"
main_file = os.path.join(base_dir, r"04-QID-Combine ORGfile\07-Requery_Filled_Combined.csv")
huma_file = os.path.join(base_dir, r"06-Huma-Fillin\02-Huma_Fillin_Merged.csv")
output_dir = os.path.join(base_dir, r"07-Human-Merge")
output_file = os.path.join(output_dir, "01-Requery_Filled_Human_Merged.csv")

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Read Main File
print(f"Reading Main File: {main_file}")
with open(main_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    main_fieldnames = reader.fieldnames
    main_data = list(reader)

# Create a lookup dictionary for Main Data (Name -> Index)
# Using a dictionary of lists to handle potential duplicates in Main (though unlikely for Refined Name)
main_lookup = {}
for idx, row in enumerate(main_data):
    name = row.get('Refined_Formal_Name', '').strip()
    if name:
        if name not in main_lookup:
            main_lookup[name] = []
        main_lookup[name].append(idx)

# Read Huma File
print(f"Reading Huma File: {huma_file}")
with open(huma_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    huma_data = list(reader)

# Process Merge
updated_count = 0
appended_count = 0
not_found_names = []

for row in huma_data:
    huma_name = row.get('Refined_Formal_Name', '').strip()
    selected_qid = row.get('Selected_QID', '').strip()
    
    if not huma_name:
        continue

    # Check if this name exists in Main
    if huma_name in main_lookup:
        # Update all matching rows in Main
        for idx in main_lookup[huma_name]:
            main_data[idx]['Original-QID'] = selected_qid
            # Optional: Clear other QID columns to avoid confusion? 
            # User only asked to replace Original-QID. Let's keep others for reference or clear them?
            # "将02-Huma_Fillin_Merged中“Selected_QID”作为正确的QID替换07-Requery_Filled_Combined，数据集中的“Original-QID”"
            # I will strictly follow this.
        updated_count += len(main_lookup[huma_name])
    else:
        # Name not found in Main (likely a split or rename)
        # We append this as a new row
        new_row = {k: '' for k in main_fieldnames} # Initialize empty row
        new_row['Refined_Formal_Name'] = huma_name
        new_row['Original-QID'] = selected_qid
        # We can try to fill other info from Huma if available, but Huma columns are different.
        # We'll leave other columns empty.
        main_data.append(new_row)
        appended_count += 1
        not_found_names.append(huma_name)

# Write Output
print(f"Writing Output File: {output_file}")
with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=main_fieldnames)
    writer.writeheader()
    writer.writerows(main_data)

print("-" * 30)
print(f"Merge Complete.")
print(f"Updated Rows: {updated_count}")
print(f"Appended New Rows: {appended_count}")
if appended_count > 0:
    print(f"Note: {appended_count} rows from Huma file were not found in Main file (likely renames or splits) and were appended.")
    # print(f"Examples of appended names: {not_found_names[:5]}")
