import csv
import os
import glob

folder_path = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\06-Huma-Fillin"
output_file = os.path.join(folder_path, "02-Huma_Fillin_Merged.csv")

# Find all files matching the pattern
files = glob.glob(os.path.join(folder_path, "01-Rows_With_Two*.csv"))
# Sort to ensure 1-100 comes before 101-200 etc. (though string sort might put 101 before 20, but here the naming is consistent enough or I can sort by number if needed. Given the names "1-100", "101-200", simple sort might be slightly off but acceptable for merging. Let's try to sort by the first number in the range)
def sort_key(filepath):
    filename = os.path.basename(filepath)
    try:
        # Extract the first number "1" from "01-Rows_With_Two 1-100.csv"
        # Split by space, take the last part "1-100.csv", split by "-", take first part
        parts = filename.split(' ')
        range_part = parts[-1]
        start_num = int(range_part.split('-')[0])
        return start_num
    except:
        return filename

files.sort(key=sort_key)

# Standardized header for the output file
header = [
    'SN', 
    'Refined_Formal_Name', 
    'Original-QID', 
    'Original-QID_Desc', 
    'Second-Query_QID', 
    'Second-Query_QID_Desc', 
    'Selected_QID', 
    'Reason'
]

all_rows = []

print(f"Found {len(files)} files to merge.")

for f in files:
    print(f"Processing {os.path.basename(f)}...")
    with open(f, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            new_row = {}
            
            # Map columns flexibly
            new_row['SN'] = row.get('SN')
            
            # Name
            new_row['Refined_Formal_Name'] = row.get('Refined_Formal_Name') or row.get('Refined_Formal_Name (正式名)')
            
            # Original QID
            new_row['Original-QID'] = row.get('Original-QID')
            new_row['Original-QID_Desc'] = row.get('Original-QID描述') or row.get('Original-QID 描述')
            
            # Second QID
            new_row['Second-Query_QID'] = row.get('Second-Query_QID')
            new_row['Second-Query_QID_Desc'] = row.get('Second-Query_QID描述') or row.get('Second-Query_QID 描述')
            
            # Result
            new_row['Selected_QID'] = row.get('保留 QID')
            new_row['Reason'] = row.get('保留原因分析 (判定标准)')
            
            all_rows.append(new_row)

# Write merged file
with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    writer.writerows(all_rows)

print(f"Successfully merged into {output_file}")
print(f"Total rows: {len(all_rows)}")
