import pandas as pd

df = pd.read_csv(r'c:\Users\001\Desktop\Github-Project\PnPDataset\06-Crosscheck\Full_Comparison_Matrix_Unique.csv')

# Check for File_Codes with multiple entries
multi_file_entries = df[df['File_Code'].str.contains(',')]

print(f"Total unique entries: {len(df)}")
print(f"Entries appearing in multiple files: {len(multi_file_entries)}")

if len(multi_file_entries) > 0:
    print("\nSample entries with multiple files:")
    print(multi_file_entries[['Index_Entry', 'File_Code']].head(10))
else:
    print("\nNo entries found with multiple file codes. This might indicate that entries are unique to each file or the aggregation logic needs checking.")

# Check for duplicates in Index_Entry to see if deduplication was strict enough
duplicates = df[df.duplicated(subset=['Index_Entry', 'CIDOC_Type'], keep=False)]
print(f"\nEntries with same name/type but different status/match (potential remaining duplicates): {len(duplicates)}")
if len(duplicates) > 0:
    print(duplicates[['Index_Entry', 'CIDOC_Type', 'Status']].head(10))
