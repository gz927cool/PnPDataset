import pandas as pd
import os

path_06 = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\04-QID-Combine ORGfile\06-Requery_Filled_Cleaned.csv"
path_03 = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\03-LLM-Fillin-QID\03-LLM_Fillin_With_QID.csv"
output_path = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\04-QID-Combine ORGfile\07-Requery_Filled_Combined.csv"

def process():
    if not os.path.exists(path_06):
        print(f"Target file not found: {path_06}")
        # Fallback to 05 if 06 doesn't exist (handling my previous confusion)
        path_05 = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\04-QID-Combine ORGfile\05-Requery_Filled_Cleaned.csv"
        if os.path.exists(path_05):
            print(f"Using 05 instead: {path_05}")
            df_target = pd.read_csv(path_05)
        else:
            print("No target file found.")
            return
    else:
        df_target = pd.read_csv(path_06)
        
    if not os.path.exists(path_03):
        print(f"Source file not found: {path_03}")
        return
    df_source = pd.read_csv(path_03)
    
    # Pre-process Source
    # Group by '原始名称 (CSV)' and aggregate QIDs
    def aggregate_qids(series):
        qids = [str(q).strip() for q in series if pd.notna(q) and str(q).strip().startswith('Q')]
        return "; ".join(sorted(set(qids))) # Unique QIDs, sorted

    # Clean source column names
    df_source.columns = [c.strip() for c in df_source.columns]
    source_key = '原始名称 (CSV)'
    
    if source_key not in df_source.columns:
        print(f"Key '{source_key}' not found in source. Columns: {df_source.columns}")
        return

    # Create mapping dictionary
    qid_map = df_source.groupby(source_key)['Matched_QID'].apply(aggregate_qids).to_dict()
    
    print(f"Loaded {len(qid_map)} mappings from Source.")
    
    # Enhanced Matching for keys with '...'
    target_key = 'Refined_Formal_Name'
    target_names = df_target[target_key].unique()
    enhanced_map = {}
    
    import re
    
    for src_name, qid in qid_map.items():
        if "..." in src_name:
            # Construct regex pattern
            # Escape the parts and join with .*
            parts = [re.escape(p.strip()) for p in src_name.split("...")]
            pattern = ".*".join(parts)
            
            # Find matches in target names
            matches = [tn for tn in target_names if isinstance(tn, str) and re.search(pattern, tn, re.IGNORECASE)]
            
            if len(matches) == 1:
                # High confidence single match
                enhanced_map[matches[0]] = qid
                # print(f"Fuzzy matched: '{src_name}' -> '{matches[0]}'")
            elif len(matches) > 1:
                # Check for exact start/end match to filter
                better_matches = [m for m in matches if m.startswith(parts[0]) and m.endswith(parts[-1])]
                if len(better_matches) == 1:
                    enhanced_map[better_matches[0]] = qid
                else:
                    print(f"Ambiguous match for '{src_name}': {len(matches)} candidates.")
        else:
            # Exact match (already handled if src_name is in target_names)
            # But we need to ensure the map uses TARGET names as keys if they differ?
            # Wait, if src_name == target_name, then it works directly.
            # If src_name is NOT in target, we can't map it unless we do fuzzy.
            # Assuming exact match for non-... names.
            if src_name in target_names:
                enhanced_map[src_name] = qid

    print(f"Enhanced map has {len(enhanced_map)} entries (including fuzzy matches).")
    
    # Create new column
    new_col_name = 'LLM-Fillin_QID'
    
    # Map values
    df_target[new_col_name] = df_target[target_key].map(enhanced_map)
    
    # Reorder columns: Insert after 'Second-Query_QID'
    cols = df_target.columns.tolist()
    if 'Second-Query_QID' in cols:
        idx = cols.index('Second-Query_QID')
        cols.insert(idx + 1, cols.pop(cols.index(new_col_name)))
        df_target = df_target[cols]
    
    # Fill NaN with empty string
    df_target[new_col_name] = df_target[new_col_name].fillna('')
    
    # Stats
    filled_count = (df_target[new_col_name] != '').sum()
    print(f"Filled {filled_count} rows with QIDs from LLM-Fillin.")
    
    # Save
    df_target.to_csv(output_path, index=False)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    process()
