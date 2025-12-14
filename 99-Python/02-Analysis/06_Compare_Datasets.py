import pandas as pd
import os
import glob
import re

def normalize_name(name):
    if not isinstance(name, str):
        return ""
    # Remove quotes
    name = name.strip().strip('"').strip("'")
    # Remove extra spaces
    name = " ".join(name.split())
    return name

def flip_name(name):
    if "," in name:
        parts = name.split(",", 1)
        if len(parts) == 2:
            return f"{parts[1].strip()} {parts[0].strip()}"
    return name

def load_handmade_data(base_dir):
    handmade_dir = os.path.join(base_dir, "05-HandmadeDataset")
    
    # Map filenames to expected CIDOC types for loose validation
    files = {
        "name-English_table.csv": ["E21 Person"],
        "gio-English_table.csv": ["E53 Place", "E74 Group"],
        "work-English_table.csv": ["E22 Man-Made Object", "E28 Conceptual Object", "E55 Type", "E1 CRM Entity"]
    }
    
    lookup = {}
    
    for filename, types in files.items():
        filepath = os.path.join(handmade_dir, filename)
        if not os.path.exists(filepath):
            print(f"Warning: {filename} not found.")
            continue
            
        try:
            df = pd.read_csv(filepath, encoding='gbk')
            # Standardize column names
            if '统一英文全名' in df.columns:
                name_col = '统一英文全名'
            else:
                print(f"Warning: '统一英文全名' column not found in {filename}")
                continue
                
            for _, row in df.iterrows():
                raw_name = row[name_col]
                qid = row['QID'] if 'QID' in row else None
                
                norm_name = normalize_name(raw_name)
                if not norm_name: continue
                
                # Store in lookup
                # Key: Normalized Name (lower case for case-insensitive matching)
                key = norm_name.lower()
                
                if key not in lookup:
                    lookup[key] = []
                
                lookup[key].append({
                    'qid': qid,
                    'source_file': filename,
                    'compatible_types': types,
                    'original_name': raw_name
                })
                
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            
    return lookup

def process_index_files(base_dir, lookup):
    index_dir = os.path.join(base_dir, "04-Index-Enrich")
    csv_files = glob.glob(os.path.join(index_dir, "*_refined.csv"))
    
    results = {
        'total_entries': 0,
        'exact_matches': 0,
        'flipped_matches': 0,
        'no_matches': 0,
        'category_mismatches': 0,
        'details': []
    }
    
    print(f"Processing {len(csv_files)} files from {index_dir}...")
    
    for filepath in csv_files:
        filename = os.path.basename(filepath)
        try:
            df = pd.read_csv(filepath)
            
            for _, row in df.iterrows():
                results['total_entries'] += 1
                
                main_entry = row.get('Index_Main Entry', '')
                cidoc_type = row.get('CIDOC_Type', '')
                
                if pd.isna(main_entry) or not str(main_entry).strip():
                    continue
                    
                norm_name = normalize_name(str(main_entry))
                key = norm_name.lower()
                
                match_found = False
                match_type = "None"
                match_info = None
                
                # 1. Try Exact Match
                if key in lookup:
                    match_found = True
                    match_type = "Exact"
                    match_info = lookup[key]
                
                # 2. Try Flipped Match (if contains comma)
                if not match_found and "," in norm_name:
                    flipped = flip_name(norm_name)
                    flipped_key = flipped.lower()
                    if flipped_key in lookup:
                        match_found = True
                        match_type = "Flipped"
                        match_info = lookup[flipped_key]
                
                if match_found:
                    # Check Category Compatibility
                    # match_info is a list of potential matches (usually 1)
                    best_match = match_info[0] # Take first for now
                    
                    is_compatible = False
                    if cidoc_type in best_match['compatible_types']:
                        is_compatible = True
                    # Loose check for Groups in Place file
                    elif cidoc_type == 'E74 Group' and 'gio-English_table.csv' == best_match['source_file']:
                        is_compatible = True
                        
                    if is_compatible:
                        if match_type == "Exact":
                            results['exact_matches'] += 1
                        else:
                            results['flipped_matches'] += 1
                    else:
                        results['category_mismatches'] += 1
                        
                    results['details'].append({
                        'File': filename,
                        'Index_Entry': main_entry,
                        'CIDOC_Type': cidoc_type,
                        'Match_Type': match_type,
                        'Matched_QID': best_match['qid'],
                        'Matched_Name': best_match['original_name'],
                        'Source_Table': best_match['source_file'],
                        'Category_Compatible': is_compatible
                    })
                else:
                    results['no_matches'] += 1
                    results['details'].append({
                        'File': filename,
                        'Index_Entry': main_entry,
                        'CIDOC_Type': cidoc_type,
                        'Match_Type': "None",
                        'Matched_QID': None,
                        'Matched_Name': None,
                        'Source_Table': None,
                        'Category_Compatible': None
                    })
                    
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    return results

def main():
    base_dir = r'c:\Users\001\Desktop\Github-Project\PnPDataset'
    
    print("Loading Handmade Dataset (05)...")
    lookup = load_handmade_data(base_dir)
    print(f"Loaded {len(lookup)} unique entries from Handmade Dataset.")
    
    print("Comparing with Index Dataset (04)...")
    results = process_index_files(base_dir, lookup)
    
    # Generate Report
    report_path = os.path.join(base_dir, r'99-Python\02-Analysis\Data_Comparison_Report.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Data Comparison Report: Index (04) vs Handmade (05)\n\n")
        f.write(f"**Total Index Entries Processed:** {results['total_entries']}\n\n")
        
        f.write("## Match Statistics\n")
        f.write(f"- **Exact Matches:** {results['exact_matches']} ({results['exact_matches']/results['total_entries']*100:.1f}%)\n")
        f.write(f"- **Flipped Matches (Last, First -> First Last):** {results['flipped_matches']} ({results['flipped_matches']/results['total_entries']*100:.1f}%)\n")
        f.write(f"- **Category Mismatches (Name matched, Type differed):** {results['category_mismatches']}\n")
        f.write(f"- **No Matches:** {results['no_matches']} ({results['no_matches']/results['total_entries']*100:.1f}%)\n\n")
        
        f.write("## Sample Matches\n")
        f.write("| Index Entry | CIDOC Type | Match Type | Matched Name | QID | Source Table |\n")
        f.write("|---|---|---|---|---|---|\n")
        
        count = 0
        for item in results['details']:
            if item['Match_Type'] != "None" and count < 20:
                f.write(f"| {item['Index_Entry']} | {item['CIDOC_Type']} | {item['Match_Type']} | {item['Matched_Name']} | {item['Matched_QID']} | {item['Source_Table']} |\n")
                count += 1
                
        f.write("\n## Sample Mismatches (Category Issues)\n")
        f.write("| Index Entry | CIDOC Type | Matched Name | Source Table |\n")
        f.write("|---|---|---|---|\n")
        
        count = 0
        for item in results['details']:
            if item['Category_Compatible'] is False and count < 10:
                f.write(f"| {item['Index_Entry']} | {item['CIDOC_Type']} | {item['Matched_Name']} | {item['Source_Table']} |\n")
                count += 1

        f.write("\n## Sample Non-Matches\n")
        f.write("| Index Entry | CIDOC Type |\n")
        f.write("|---|---|\n")
        
        count = 0
        for item in results['details']:
            if item['Match_Type'] == "None" and count < 20:
                f.write(f"| {item['Index_Entry']} | {item['CIDOC_Type']} |\n")
                count += 1
                
    print(f"Report generated at {report_path}")

if __name__ == "__main__":
    main()
