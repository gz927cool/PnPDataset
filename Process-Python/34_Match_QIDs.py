import pandas as pd
import os

# Define paths
base_dir = r"c:\Users\001\Desktop\Github-Project\PnPDataset"
# Changed to CSV as XLSX seems missing or problematic
input_file = os.path.join(base_dir, "08-Data-Remerge", "03-Merged_Recheck_Simplified.csv") 
handmade_dir = os.path.join(base_dir, "05-HandmadeDataset")
output_file = os.path.join(base_dir, "08-Data-Remerge", "04-Merged_Recheck_With_QID.xlsx")

def load_handmade_mapping():
    mapping = {}
    files = [
        ("name-English_table.csv", 2), # Name is at index 2
        ("gio-English_table.csv", 2),  # Name is at index 2
        ("work-English_table.csv", 1)  # Name is at index 1
    ]
    
    print("Building QID mapping from Handmade Dataset...")
    
    for filename, name_col_idx in files:
        filepath = os.path.join(handmade_dir, filename)
        if not os.path.exists(filepath):
            print(f"Warning: {filename} not found.")
            continue
            
        try:
            # Try GBK first as these files often have Chinese headers/content in GBK
            df = pd.read_csv(filepath, encoding='gbk')
        except:
            try:
                df = pd.read_csv(filepath, encoding='utf-8-sig')
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue
        
        # Get QID column (always index 0) and Name column
        # Ensure we access by position since headers might be garbled
        qid_col = df.columns[0]
        name_col = df.columns[name_col_idx]
        
        count = 0
        for _, row in df.iterrows():
            qid = str(row[qid_col]).strip()
            name = str(row[name_col]).strip()
            
            if pd.notna(name) and name != "" and pd.notna(qid) and qid != "":
                # Store in mapping. If duplicate names exist, later ones might overwrite earlier ones.
                # Given it's a handmade dataset, we assume it's relatively clean or we accept the last one.
                mapping[name] = qid
                count += 1
        
        print(f"Loaded {count} entries from {filename}")
        
    print(f"Total unique names in mapping: {len(mapping)}")
    return mapping

def match_qids():
    # 1. Load Main Dataset
    print(f"Loading main dataset from {input_file}...")
    try:
        df = pd.read_csv(input_file, encoding='utf-8-sig')
    except:
        df = pd.read_csv(input_file, encoding='gbk')
        
    print(f"Rows: {len(df)}")
    
    # 2. Load Mapping
    qid_map = load_handmade_mapping()
    
    # 3. Perform Matching
    print("Matching QIDs...")
    
    def get_qid(name):
        if pd.isna(name):
            return None
        name = str(name).strip()
        return qid_map.get(name, None)

    df['QID'] = df['Refined_Formal_Name'].apply(get_qid)
    
    # 4. Statistics
    matched_count = df['QID'].notna().sum()
    total_count = len(df)
    match_rate = (matched_count / total_count) * 100
    
    print("-" * 30)
    print(f"Total Rows: {total_count}")
    print(f"Matched QIDs: {matched_count}")
    print(f"Unmatched: {total_count - matched_count}")
    print(f"Match Rate: {match_rate:.2f}%")
    print("-" * 30)
    
    # 5. Save Result
    # Reorder columns to put QID next to Name
    cols = ['Refined_Formal_Name', 'QID', 'Refined_Category', 'Status/Notes']
    # Add any other columns that might exist (though simplified usually has just these)
    remaining_cols = [c for c in df.columns if c not in cols]
    final_cols = cols + remaining_cols
    
    df = df[final_cols]
    
    print(f"Saving to {output_file}...")
    df.to_excel(output_file, index=False)
    print("Done.")

if __name__ == "__main__":
    match_qids()
