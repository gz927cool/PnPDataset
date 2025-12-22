import pandas as pd
import os
import glob

# Paths
base_dir = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin"
input_dir = os.path.join(base_dir, "LLM-fillin")
output_file = os.path.join(base_dir, "02-LLM_Fillin_Merged_Split.csv")

def split_description(text):
    if not isinstance(text, str):
        return text, ""
    
    # Try splitting by " / " or just "/"
    # Based on observation: "Chinese text. / English text."
    if "/" in text:
        parts = text.rsplit("/", 1) # Split from right to handle potential slashes in Chinese part?
        # Actually, usually English is the second part.
        # Let's check if the slash is a separator.
        if len(parts) == 2:
            cn = parts[0].strip()
            en = parts[1].strip()
            return cn, en
    
    return text, ""

def main():
    print(f"Scanning {input_dir}...")
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))
    
    all_dfs = []
    
    for f in csv_files:
        print(f"Reading {os.path.basename(f)}...")
        try:
            # Try utf-8 first, then gbk if fails
            df = pd.read_csv(f, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(f, encoding='gbk')
            
        all_dfs.append(df)
        
    if not all_dfs:
        print("No CSV files found.")
        return

    combined_df = pd.concat(all_dfs, ignore_index=True)
    print(f"Total rows: {len(combined_df)}")
    
    # 1. Split Description
    desc_col = "内容描述 (中/英)"
    if desc_col in combined_df.columns:
        print(f"Splitting '{desc_col}'...")
        # Apply split function
        split_data = combined_df[desc_col].apply(lambda x: split_description(x))
        
        # Create new columns
        combined_df['Description_CN'] = [x[0] for x in split_data]
        combined_df['Description_EN'] = [x[1] for x in split_data]
        
        # Drop original? User didn't ask to drop original description, but "分为2列" usually implies replacement or addition.
        # I will keep new columns and maybe drop the old one to be clean?
        # User said "分为2列", I will keep the new ones.
        # I'll drop the old one to avoid clutter.
        combined_df.drop(columns=[desc_col], inplace=True)
    else:
        print(f"Warning: Column '{desc_col}' not found.")
        
    # 2. Delete QID Column
    qid_col = "QID/标识"
    if qid_col in combined_df.columns:
        print(f"Dropping '{qid_col}'...")
        combined_df.drop(columns=[qid_col], inplace=True)
    else:
        print(f"Warning: Column '{qid_col}' not found.")

    # 3. Drop Row Number Columns
    cols_to_drop = ["原始行号", "原始 CSV 行号"]
    print(f"Columns in dataframe: {combined_df.columns.tolist()}")
    
    # Normalize columns (strip whitespace)
    combined_df.columns = [c.strip() for c in combined_df.columns]
    
    for col in cols_to_drop:
        if col in combined_df.columns:
            print(f"Dropping '{col}'...")
            combined_df.drop(columns=[col], inplace=True)
        else:
            print(f"Warning: Column '{col}' not found.")
            # Hard try to find and drop by partial match or index
            matching_cols = [c for c in combined_df.columns if col in c]
            if matching_cols:
                print(f"Dropping matching cols: {matching_cols}")
                combined_df.drop(columns=matching_cols, inplace=True)

    # Re-check columns
    print(f"Final columns: {combined_df.columns.tolist()}")

    # Save
    print(f"Saving to {output_file}...")
    combined_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print("Done.")

if __name__ == "__main__":
    main()
