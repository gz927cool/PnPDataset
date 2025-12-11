import os
import pandas as pd

enrich_dir = r"c:\Users\001\Desktop\list\04-Enrich"

def audit_missing():
    print("--- Audit of Missing Locations ---")
    files = [f for f in os.listdir(enrich_dir) if f.endswith("_refined.csv")]
    
    total_missing = 0
    total_rows = 0
    
    print(f"{'File':<20} | {'Total Rows':<10} | {'Missing Loc':<12} | {'% Complete':<10}")
    print("-" * 60)
    
    for filename in files:
        path = os.path.join(enrich_dir, filename)
        try:
            df = pd.read_csv(path)
            missing_count = df['Proposed Location'].isna().sum() + (df['Proposed Location'] == "").sum()
            row_count = len(df)
            
            percent = ((row_count - missing_count) / row_count) * 100 if row_count > 0 else 0
            
            print(f"{filename:<20} | {row_count:<10} | {missing_count:<12} | {percent:.1f}%")
            
            total_missing += missing_count
            total_rows += row_count
            
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    print("-" * 60)
    total_percent = ((total_rows - total_missing) / total_rows) * 100 if total_rows > 0 else 0
    print(f"{'TOTAL':<20} | {total_rows:<10} | {total_missing:<12} | {total_percent:.1f}%")

if __name__ == "__main__":
    audit_missing()
