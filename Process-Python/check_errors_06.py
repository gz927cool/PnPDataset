import pandas as pd
import os
import re

# Define paths
file_path = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\07-Human-Merge\06-Requery_Filled_Human_Merged_Corrected.csv"

print(f"Analyzing file: {file_path}")

try:
    df = pd.read_csv(file_path)
except Exception as e:
    print(f"Error reading file: {e}")
    exit()

# Basic Stats
print("-" * 30)
print(f"Total Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")

# 1. Check for Missing QIDs
missing_qid = df[df['Original-QID'].isna() | (df['Original-QID'].astype(str).str.strip() == '')]
print("-" * 30)
print(f"Rows with Missing QIDs: {len(missing_qid)}")
if len(missing_qid) > 0:
    print(missing_qid[['Refined_Formal_Name']].head(5))

# 2. Check for QID Format Errors
# Valid QID: Q followed by digits
def is_valid_qid(qid):
    if pd.isna(qid) or str(qid).strip() == '':
        return True # Skip missing, handled above
    return bool(re.match(r'^Q\d+$', str(qid)))

invalid_format = df[~df['Original-QID'].apply(is_valid_qid)]
print("-" * 30)
print(f"Rows with Invalid QID Format: {len(invalid_format)}")
if len(invalid_format) > 0:
    print(invalid_format[['Refined_Formal_Name', 'Original-QID']].head(5))

# 3. Check for QID Collisions (Same QID, Different Names)
# We ignore case and whitespace for name comparison
print("-" * 30)
print("Checking for QID Collisions (Same QID, Multiple Names)...")

# Filter out missing QIDs for this check
df_clean = df.dropna(subset=['Original-QID'])
df_clean = df_clean[df_clean['Original-QID'].str.startswith('Q')]

qid_groups = df_clean.groupby('Original-QID')['Refined_Formal_Name'].unique()
collisions = qid_groups[qid_groups.apply(len) > 1]

print(f"Found {len(collisions)} QIDs associated with multiple names.")
if len(collisions) > 0:
    print("Top 10 Collisions:")
    for qid, names in collisions.head(10).items():
        print(f"  {qid}: {list(names)}")

# 4. Check for Name Collisions (Same Name, Different QIDs)
print("-" * 30)
print("Checking for Name Collisions (Same Name, Multiple QIDs)...")
name_groups = df_clean.groupby('Refined_Formal_Name')['Original-QID'].unique()
name_collisions = name_groups[name_groups.apply(len) > 1]

print(f"Found {len(name_collisions)} Names associated with multiple QIDs.")
if len(name_collisions) > 0:
    print("Top 10 Name Collisions:")
    for name, qids in name_collisions.head(10).items():
        print(f"  {name}: {list(qids)}")

print("-" * 30)
print("Analysis Complete.")
