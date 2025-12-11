import os
import pandas as pd

enrich_dir = r"c:\Users\001\Desktop\list\04-Enrich"

# Column mapping
column_mapping = {
    "Main Entry": "Index_Main Entry",
    "Location": "Index_Location",
    "Sub-entry": "Index_Sub-entry",
    "Detail": "Index_Detail",
    "Page Numbers": "Index_Page Numbers",
    "Type": "CIDOC_Type"
}

def rename_columns():
    print("--- Renaming Columns in 04-Enrich ---")
    files = [f for f in os.listdir(enrich_dir) if f.endswith("_refined.csv")]
    
    total_files = 0
    
    for filename in files:
        path = os.path.join(enrich_dir, filename)
        try:
            df = pd.read_csv(path)
            
            # Check which columns are present and need renaming
            # We use a subset of the mapping based on what's actually in the file
            # to avoid errors if a column is missing, though rename() usually handles that gracefully.
            
            original_cols = df.columns.tolist()
            df.rename(columns=column_mapping, inplace=True)
            new_cols = df.columns.tolist()
            
            if original_cols != new_cols:
                df.to_csv(path, index=False, encoding='utf-8-sig')
                print(f"Updated columns in {filename}")
                total_files += 1
            else:
                print(f"No changes needed for {filename}")
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    print(f"Total files updated: {total_files}")

if __name__ == "__main__":
    rename_columns()
