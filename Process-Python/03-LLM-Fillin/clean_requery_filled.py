import pandas as pd
import os

input_path = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\04-QID-Combine ORGfile\05-Requery_Filled.csv"
output_path = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\04-QID-Combine ORGfile\05-Requery_Filled_Cleaned.csv"

def process():
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        return

    df = pd.read_csv(input_path)
    
    # 1. Drop columns
    cols_to_drop = [
        "Second-Query_Logic", 
        "Second-Query_Description", 
        "Original-Status/Notes", 
        "Original-Refined_Category"
    ]
    
    print(f"Columns before: {df.columns.tolist()}")
    
    # Check if columns exist before dropping to avoid errors
    existing_cols_to_drop = [c for c in cols_to_drop if c in df.columns]
    if existing_cols_to_drop:
        df.drop(columns=existing_cols_to_drop, inplace=True)
        print(f"Dropped: {existing_cols_to_drop}")
    else:
        print("No target columns found to drop.")
        
    # 2. Clean Second-Query_QID
    # Ensure string type for comparison
    df['Original-QID'] = df['Original-QID'].astype(str).str.strip().replace('nan', '')
    df['Second-Query_QID'] = df['Second-Query_QID'].astype(str).str.strip().replace('nan', '')
    
    # Logic: If Second == Original, clear Second.
    mask_same = (df['Second-Query_QID'] != '') & (df['Second-Query_QID'] == df['Original-QID'])
    count_cleared = mask_same.sum()
    
    df.loc[mask_same, 'Second-Query_QID'] = ''
    
    remaining_second = (df['Second-Query_QID'] != '').sum()
    
    print(f"Cleared {count_cleared} redundant Second-Query_QIDs.")
    print(f"Remaining distinct Second-Query_QIDs: {remaining_second}")
    print(f"Columns after: {df.columns.tolist()}")
    
    df.to_csv(output_path, index=False)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    process()
