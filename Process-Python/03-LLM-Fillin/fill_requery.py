import pandas as pd
import os

file_path = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\04-QID-Combine ORGfile\04-Requery_Results_Advanced.csv"
output_path = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\04-QID-Combine ORGfile\05-Requery_Filled.csv"

def process():
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    df = pd.read_csv(file_path)
    
    # Normalize QIDs
    df['Original-QID'] = df['Original-QID'].astype(str).str.strip().replace('nan', '')
    df['Second-Query_QID'] = df['Second-Query_QID'].astype(str).str.strip().replace('nan', '')
    
    # Count before
    empty_before = len(df[df['Original-QID'] == ''])
    
    # Fill logic: If Original is empty AND Second is not empty -> Fill
    mask_fill = (df['Original-QID'] == '') & (df['Second-Query_QID'] != '')
    df.loc[mask_fill, 'Original-QID'] = df.loc[mask_fill, 'Second-Query_QID']
    df.loc[mask_fill, 'Original-Status/Notes'] = "[Filled] QID filled from Second Query"
    
    # Count after
    filled_count = mask_fill.sum()
    empty_after = len(df[df['Original-QID'] == ''])
    
    print(f"Filled {filled_count} missing QIDs.")
    print(f"Empty before: {empty_before}, Empty after: {empty_after}")
    
    # Save
    df.to_csv(output_path, index=False)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    process()
