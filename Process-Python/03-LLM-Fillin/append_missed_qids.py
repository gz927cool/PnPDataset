import pandas as pd
import os
import re

path_source = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\03-LLM-Fillin-QID\03-LLM_Fillin_With_QID.csv"
path_target = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\04-QID-Combine ORGfile\07-Requery_Filled_Combined.csv"

def process():
    if not os.path.exists(path_source) or not os.path.exists(path_target):
        print("Files not found.")
        return

    df_src = pd.read_csv(path_source)
    df_tgt = pd.read_csv(path_target)
    
    # Identify unmapped source items
    df_src_valid = df_src[df_src['Matched_QID'].astype(str).str.strip().str.startswith('Q', na=False)].copy()
    
    # Target names set for fast lookup
    tgt_names = set(df_tgt['Refined_Formal_Name'].unique())
    
    # Logic to find missed items (same as verify script)
    missed_rows = []
    
    for idx, row in df_src_valid.iterrows():
        name = row['原始名称 (CSV)']
        qid = row['Matched_QID']
        
        # Exact match
        if name in tgt_names:
            continue
            
        # Fuzzy match
        matched = False
        if isinstance(name, str) and "..." in name:
            parts = [re.escape(p.strip()) for p in name.split("...")]
            pattern = ".*".join(parts)
            for tn in tgt_names:
                if isinstance(tn, str) and re.search(pattern, tn, re.IGNORECASE):
                    matched = True
                    break
        
        if not matched:
            missed_rows.append({
                'Refined_Formal_Name': name,
                'Original-QID': '',
                'Second-Query_QID': '',
                'LLM-Fillin_QID': qid,
                'Second-Query_Label': row.get('Matched_Label', '') # Optional: Add label if available
            })
    
    print(f"Found {len(missed_rows)} missed rows to append.")
    
    if missed_rows:
        df_append = pd.DataFrame(missed_rows)
        # Ensure column order matches target
        # Add missing columns to df_append with empty values
        for col in df_tgt.columns:
            if col not in df_append.columns:
                df_append[col] = ''
        
        # Select only target columns
        df_append = df_append[df_tgt.columns]
        
        # Append
        df_final = pd.concat([df_tgt, df_append], ignore_index=True)
        
        df_final.to_csv(path_target, index=False)
        print(f"Appended rows. New total: {len(df_final)}")
        print(f"Saved to {path_target}")
    else:
        print("No rows to append.")

if __name__ == "__main__":
    process()
