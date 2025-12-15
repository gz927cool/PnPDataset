import pandas as pd
import os
import glob
import re

# --- Configuration & Dictionaries ---

TITLES = [
    'Sir', 'Lord', 'Lady', 'Duke', 'Duchess', 'Count', 'Countess', 'Earl', 'Baron', 
    'Prince', 'Princess', 'King', 'Queen', 'Cardinal', 'Pope', 'Bishop', 'Abbot', 
    'Fra', 'Don', 'Donna', 'Marchese', 'Marchesa', 'Cavaliere', 'Abate', 'Monsignor'
]

ABBREVIATIONS = {
    r'\bS\.\s': 'San ',       
    r'\bSt\.\s': 'Saint ',    
    r'\bSta\.\s': 'Santa ',   
    r'\bSS\.\s': 'Santi ',    
    r'\bPza\.\s': 'Piazza ',  
    r'\bPal\.\s': 'Palazzo ', 
    r'\bCh\.\s': 'Church ',   
    r'\bAcad\.\s': 'Academy ' 
}

# --- Normalization Functions ---

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.strip().strip('"').strip("'")
    text = " ".join(text.split())
    return text

def strip_titles(name):
    for title in TITLES:
        pattern = r'\b' + re.escape(title) + r'\b\.?'
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)
    return " ".join(name.split())

def expand_abbreviations(name):
    for pattern, replacement in ABBREVIATIONS.items():
        name = re.sub(pattern, replacement, name, flags=re.IGNORECASE)
    return name

def flip_name(name):
    if "," in name:
        parts = name.split(",", 1)
        if len(parts) == 2:
            return f"{parts[1].strip()} {parts[0].strip()}"
    return name

def normalize_person(name):
    if "," in name:
        name = flip_name(name)
    name = strip_titles(name)
    return name.lower().strip()

def normalize_place_group(name):
    name = expand_abbreviations(name)
    if name.lower().startswith("the "):
        name = name[4:]
    return name.lower().strip()

def normalize_work(name):
    if name.lower().startswith("the "):
        name = name[4:]
    return name.lower().strip()

# --- Matching Logic ---

def load_handmade_data(base_dir):
    handmade_dir = os.path.join(base_dir, "05-HandmadeDataset")
    
    files_config = {
        "name-English_table.csv": {
            "types": ["E21 Person"],
            "norm_func": normalize_person
        },
        "gio-English_table.csv": {
            "types": ["E53 Place", "E74 Group"],
            "norm_func": normalize_place_group
        },
        "work-English_table.csv": {
            "types": ["E22 Man-Made Object", "E28 Conceptual Object", "E55 Type", "E1 CRM Entity"],
            "norm_func": normalize_work
        }
    }
    
    lookup = {}
    
    for filename, config in files_config.items():
        filepath = os.path.join(handmade_dir, filename)
        if not os.path.exists(filepath):
            continue
            
        try:
            df = pd.read_csv(filepath, encoding='gbk')
            if '统一英文全名' in df.columns:
                name_col = '统一英文全名'
            else:
                continue
                
            for _, row in df.iterrows():
                raw_name = row[name_col]
                qid = row.get('QID')
                
                if not isinstance(raw_name, str): continue
                
                norm_name = config['norm_func'](raw_name)
                
                if not norm_name: continue
                
                if norm_name not in lookup:
                    lookup[norm_name] = []
                
                lookup[norm_name].append({
                    'qid': qid,
                    'source_file': filename,
                    'compatible_types': config['types'],
                    'original_name': raw_name
                })
                
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            
    return lookup

def generate_crosscheck_files(base_dir, lookup):
    index_dir = os.path.join(base_dir, "04-Index-Enrich")
    output_dir = os.path.join(base_dir, "06-Crosscheck")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    csv_files = glob.glob(os.path.join(index_dir, "*_refined.csv"))
    
    print(f"Processing {len(csv_files)} files...")
    
    for filepath in csv_files:
        filename = os.path.basename(filepath)
        try:
            df = pd.read_csv(filepath)
            
            # New columns
            df['Matched_QID'] = None
            df['Matched_Name'] = None
            df['Match_Source'] = None
            df['Match_Type'] = None
            
            for index, row in df.iterrows():
                main_entry = row.get('Index_Main Entry', '')
                cidoc_type = row.get('CIDOC_Type', '')
                
                if pd.isna(main_entry) or not str(main_entry).strip():
                    continue
                
                raw_name = str(main_entry)
                
                # Determine normalization
                norm_name = ""
                if cidoc_type == 'E21 Person':
                    norm_name = normalize_person(raw_name)
                elif cidoc_type in ['E53 Place', 'E74 Group']:
                    norm_name = normalize_place_group(raw_name)
                else:
                    norm_name = normalize_work(raw_name)
                
                match_info = None
                match_type = None
                
                # 1. Try Normalized Match
                if norm_name in lookup:
                    match_info = lookup[norm_name][0]
                    match_type = "Direct Match"
                
                # 2. Fallback: Cross-Category Check (Person <-> Place)
                if not match_info and cidoc_type == 'E53 Place':
                    alt_norm = normalize_person(raw_name)
                    if alt_norm in lookup:
                        match_info = lookup[alt_norm][0]
                        match_type = "Cross-Category Match"

                if match_info:
                    df.at[index, 'Matched_QID'] = match_info['qid']
                    df.at[index, 'Matched_Name'] = match_info['original_name']
                    df.at[index, 'Match_Source'] = match_info['source_file']
                    df.at[index, 'Match_Type'] = match_type
            
            # Save to 06-Crosscheck
            output_filename = filename.replace("_refined.csv", "_crosscheck.csv")
            output_path = os.path.join(output_dir, output_filename)
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"Saved: {output_filename}")
                    
        except Exception as e:
            print(f"Error processing {filename}: {e}")

def main():
    base_dir = r'c:\Users\001\Desktop\Github-Project\PnPDataset'
    
    print("Loading Handmade Dataset...")
    lookup = load_handmade_data(base_dir)
    
    print("Generating Crosscheck Files...")
    generate_crosscheck_files(base_dir, lookup)
    print("Done.")

if __name__ == "__main__":
    main()
