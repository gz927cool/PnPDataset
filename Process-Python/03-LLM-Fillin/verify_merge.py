import pandas as pd
import os

path_source = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\03-LLM-Fillin-QID\03-LLM_Fillin_With_QID.csv"
path_target = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\04-QID-Combine ORGfile\07-Requery_Filled_Combined.csv"

def verify():
    print("Loading datasets...")
    df_src = pd.read_csv(path_source)
    df_tgt = pd.read_csv(path_target)
    
    # 1. Identify Source Rows with QIDs
    # Filter where Matched_QID is valid (starts with Q)
    df_src_valid = df_src[df_src['Matched_QID'].astype(str).str.strip().str.startswith('Q', na=False)].copy()
    
    total_source_qids = len(df_src_valid)
    print(f"\n[Source] Total rows with valid QIDs: {total_source_qids}")
    
    # 2. Identify Target Rows that received QIDs
    # The column is 'LLM-Fillin_QID'
    df_tgt_filled = df_tgt[df_tgt['LLM-Fillin_QID'].notna() & (df_tgt['LLM-Fillin_QID'] != '')].copy()
    
    total_target_filled = len(df_tgt_filled)
    print(f"[Target] Total rows filled with QIDs: {total_target_filled}")
    
    # 3. Analyze Coverage
    # We need to check which Source items were NOT mapped.
    # Logic: Source Key -> Target Key.
    # In the merge script, we mapped Source['原始名称 (CSV)'] -> Target['Refined_Formal_Name']
    
    # Let's reconstruct the mapping check to see what failed
    src_names_with_qid = df_src_valid['原始名称 (CSV)'].unique()
    tgt_names = set(df_tgt['Refined_Formal_Name'].unique())
    
    missed_names = []
    
    import re
    
    for name in src_names_with_qid:
        # Check Exact Match
        if name in tgt_names:
            continue
            
        # Check Fuzzy Match (logic from previous script)
        matched = False
        if "..." in name:
            parts = [re.escape(p.strip()) for p in name.split("...")]
            pattern = ".*".join(parts)
            # Simple regex check against all target names is slow, but fine for verification
            for tn in tgt_names:
                if isinstance(tn, str) and re.search(pattern, tn, re.IGNORECASE):
                    matched = True
                    break
        
        if not matched:
            missed_names.append(name)
            
    print(f"\n[Analysis] Mismatched Names: {len(missed_names)}")
    if len(missed_names) > 0:
        print("Samples of names present in Source (with QID) but NOT matched to Target:")
        for n in missed_names[:10]:
            qid = df_src_valid[df_src_valid['原始名称 (CSV)'] == n]['Matched_QID'].iloc[0]
            print(f" - [{qid}] {n}")
            
    # 4. Check for 'One-to-Many' or 'Many-to-One' effects
    # Did multiple source rows merge into one target row?
    # Or did one source row fail to find ANY target row?
    
    # Let's count unique QIDs to handle row splitting/merging issues
    src_qids = set(df_src_valid['Matched_QID'].str.strip().unique())
    
    # Target QIDs might be semicolon separated "Q1; Q2"
    tgt_qids = set()
    for val in df_tgt_filled['LLM-Fillin_QID']:
        if isinstance(val, str):
            for q in val.split(';'):
                tgt_qids.add(q.strip())
                
    missing_qids = src_qids - tgt_qids
    print(f"\n[QID Check] Unique QIDs in Source: {len(src_qids)}")
    print(f"[QID Check] Unique QIDs in Target: {len(tgt_qids)}")
    print(f"[QID Check] QIDs missing from Target: {len(missing_qids)}")
    
    if len(missing_qids) > 0:
        print("Sample Missing QIDs:")
        print(list(missing_qids)[:10])

if __name__ == "__main__":
    verify()
