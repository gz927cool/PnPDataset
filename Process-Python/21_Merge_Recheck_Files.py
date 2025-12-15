import pandas as pd
import os
import glob

def merge_recheck_files():
    base_dir = r'c:\Users\001\Desktop\Github-Project\PnPDataset'
    input_dir = os.path.join(base_dir, r'07-MML')
    output_dir = os.path.join(base_dir, r'08-Recheck')
    output_csv = os.path.join(output_dir, r'01-Merged_Recheck.csv')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
        
    if not os.path.exists(input_dir):
        print(f"Input directory not found: {input_dir}")
        return

    print(f"Scanning {input_dir} for CSV files...")
    csv_files = glob.glob(os.path.join(input_dir, '*.csv'))
    
    if not csv_files:
        print("No CSV files found.")
        return
        
    print(f"Found {len(csv_files)} files.")
    
    all_dfs = []
    for f in csv_files:
        try:
            # Try reading with utf-8-sig first, then gbk if fails
            try:
                df = pd.read_csv(f, encoding='utf-8-sig')
            except UnicodeDecodeError:
                df = pd.read_csv(f, encoding='gbk')
                
            all_dfs.append(df)
            # print(f"  Loaded {os.path.basename(f)} ({len(df)} rows)")
        except Exception as e:
            print(f"  Error reading {os.path.basename(f)}: {e}")
            
    if all_dfs:
        merged_df = pd.concat(all_dfs, ignore_index=True)
        print(f"\nMerged total: {len(merged_df)} rows.")
        
        merged_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
        print(f"Saved merged file to: {output_csv}")
    else:
        print("No data merged.")

if __name__ == "__main__":
    merge_recheck_files()
