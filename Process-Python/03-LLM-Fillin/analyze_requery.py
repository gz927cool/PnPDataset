import pandas as pd
import os

file_path = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\04-QID-Combine ORGfile\04-Requery_Results_Advanced.csv"

def analyze():
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    df = pd.read_csv(file_path)
    
    total = len(df)
    
    # Normalize QIDs (strip, uppercase)
    df['Original-QID'] = df['Original-QID'].astype(str).str.strip().replace('nan', '')
    df['Second-Query_QID'] = df['Second-Query_QID'].astype(str).str.strip().replace('nan', '')
    
    # Analysis
    same = df[ (df['Original-QID'] != '') & (df['Original-QID'] == df['Second-Query_QID']) ]
    diff = df[ (df['Original-QID'] != '') & (df['Second-Query_QID'] != '') & (df['Original-QID'] != df['Second-Query_QID']) ]
    orig_empty_second_has = df[ (df['Original-QID'] == '') & (df['Second-Query_QID'] != '') ]
    orig_has_second_empty = df[ (df['Original-QID'] != '') & (df['Second-Query_QID'] == '') ]
    both_empty = df[ (df['Original-QID'] == '') & (df['Second-Query_QID'] == '') ]
    
    print(f"Total Rows: {total}")
    print(f"1. Match (Original == Second): {len(same)}")
    print(f"2. Conflict (Original != Second): {len(diff)}")
    print(f"3. Fillable (Original Empty, Second Has): {len(orig_empty_second_has)}")
    print(f"4. Unverified (Original Has, Second Empty): {len(orig_has_second_empty)}")
    print(f"5. No Data (Both Empty): {len(both_empty)}")
    
    # Check sample of 'Fillable'
    if len(orig_empty_second_has) > 0:
        print("\nSample Fillable:")
        print(orig_empty_second_has[['Refined_Formal_Name', 'Second-Query_QID']].head())

if __name__ == "__main__":
    analyze()
