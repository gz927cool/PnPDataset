import pandas as pd
import os

# Define paths
base_dir = r"c:\Users\001\Desktop\Github-Project\PnPDataset"
# The user mentioned "01-Merged_Recheck_With_QID", but the file generated was 04.
# We will look for 04.
input_file = os.path.join(base_dir, "08-Data-Remerge", "04-Merged_Recheck_With_QID.csv")
output_file = os.path.join(base_dir, "08-Data-Remerge", "04-Merged_Recheck_With_QID_Cleaned.csv")

def filter_qids():
    print(f"Looking for file: {input_file}")
    
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found.")
        # Fallback check
        fallback = os.path.join(base_dir, "08-Data-Remerge", "04-Merged_Recheck_With_QID.xlsx")
        if os.path.exists(fallback):
            print(f"Found .xlsx version instead. Loading {fallback}...")
            df = pd.read_excel(fallback)
        else:
            print("Could not find input file.")
            return
    else:
        print(f"Loading {input_file}...")
        try:
            df = pd.read_csv(input_file, encoding='utf-8-sig')
        except:
            df = pd.read_csv(input_file, encoding='gbk')

    print(f"Original rows: {len(df)}")
    
    if 'QID' not in df.columns:
        print("Error: 'QID' column not found.")
        return

    # Function to clean QID
    def clean_qid(val):
        if pd.isna(val):
            return None
        s = str(val).strip()
        if s.startswith('Q'):
            return s
        else:
            # User said: Delete A G R data, only keep Q data.
            # Implies anything not starting with Q is removed.
            return None

    # Apply filter
    print("Filtering QID column...")
    original_qids = df['QID'].notna().sum()
    df['QID'] = df['QID'].apply(clean_qid)
    remaining_qids = df['QID'].notna().sum()
    
    print(f"QIDs before: {original_qids}")
    print(f"QIDs after: {remaining_qids}")
    print(f"Removed {original_qids - remaining_qids} invalid QIDs.")

    # Save
    print(f"Saving to {output_file}...")
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print("Done.")

if __name__ == "__main__":
    filter_qids()
