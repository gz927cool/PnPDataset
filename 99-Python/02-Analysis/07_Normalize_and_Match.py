import pandas as pd
import os
import glob
import re

# --- Configuration & Dictionaries ---

# Titles to strip for Person matching
TITLES = [
    'Sir', 'Lord', 'Lady', 'Duke', 'Duchess', 'Count', 'Countess', 'Earl', 'Baron', 
    'Prince', 'Princess', 'King', 'Queen', 'Cardinal', 'Pope', 'Bishop', 'Abbot', 
    'Fra', 'Don', 'Donna', 'Marchese', 'Marchesa', 'Cavaliere', 'Abate', 'Monsignor'
]

# Abbreviations to expand for Place/Group matching
ABBREVIATIONS = {
    r'\bS\.\s': 'San ',       # S. -> San (Italian context default)
    r'\bSt\.\s': 'Saint ',    # St. -> Saint
    r'\bSta\.\s': 'Santa ',   # Sta. -> Santa
    r'\bSS\.\s': 'Santi ',    # SS. -> Santi
    r'\bPza\.\s': 'Piazza ',  # Pza. -> Piazza
    r'\bPal\.\s': 'Palazzo ', # Pal. -> Palazzo
    r'\bCh\.\s': 'Church ',   # Ch. -> Church
    r'\bAcad\.\s': 'Academy ' # Acad. -> Academy
}

# Stopwords that might cause noise in "Contains" matching
STOPWORDS = {'the', 'of', 'de', 'di', 'da', 'del', 'della', 'and', '&', 'a', 'in'}

# --- Normalization Functions ---

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # Remove quotes and extra spaces
    text = text.strip().strip('"').strip("'")
    text = " ".join(text.split())
    return text

def strip_titles(name):
    """Removes known titles from the name."""
    # Create a regex pattern for titles (case insensitive)
    # We look for Title at start of string or after a space
    for title in TITLES:
        # Pattern: Word boundary + Title + (Space or End of string)
        pattern = r'\b' + re.escape(title) + r'\b\.?'
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)
    return " ".join(name.split())

def expand_abbreviations(name):
    """Expands common abbreviations."""
    for pattern, replacement in ABBREVIATIONS.items():
        name = re.sub(pattern, replacement, name, flags=re.IGNORECASE)
    return name

def flip_name(name):
    """Flips 'Last, First' to 'First Last'."""
    if "," in name:
        parts = name.split(",", 1)
        if len(parts) == 2:
            return f"{parts[1].strip()} {parts[0].strip()}"
    return name

def normalize_person(name):
    """Pipeline for Person names."""
    # 1. Flip if comma exists (Index format: Last, First)
    if "," in name:
        name = flip_name(name)
    
    # 2. Strip Titles (e.g., "Cardinal Annibale Albani" -> "Annibale Albani")
    name = strip_titles(name)
    
    return name.lower().strip()

def normalize_place_group(name):
    """Pipeline for Places and Groups."""
    # 1. Expand Abbreviations (e.g., "S. Luca" -> "San Luca")
    name = expand_abbreviations(name)
    
    # 2. Remove "The" at start (optional, but often helpful)
    if name.lower().startswith("the "):
        name = name[4:]
        
    return name.lower().strip()

def normalize_work(name):
    """Pipeline for Works/Concepts."""
    # Similar to Place/Group but maybe less aggressive on abbreviations
    if name.lower().startswith("the "):
        name = name[4:]
    return name.lower().strip()

# --- Matching Logic ---

def load_handmade_data(base_dir):
    handmade_dir = os.path.join(base_dir, "05-HandmadeDataset")
    
    # Define file mappings and their specific normalization logic
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
            print(f"Warning: {filename} not found.")
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
                
                # Apply specific normalization
                norm_name = config['norm_func'](raw_name)
                
                if not norm_name: continue
                
                if norm_name not in lookup:
                    lookup[norm_name] = []
                
                lookup[norm_name].append({
                    'qid': qid,
                    'source_file': filename,
                    'compatible_types': config['types'],
                    'original_name': raw_name,
                    'norm_method': 'Advanced'
                })
                
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            
    return lookup

def process_index_files(base_dir, lookup):
    index_dir = os.path.join(base_dir, "04-Index-Enrich")
    csv_files = glob.glob(os.path.join(index_dir, "*_refined.csv"))
    
    results = {
        'total_entries': 0,
        'matches': 0,
        'no_matches': 0,
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
                
                raw_name = str(main_entry)
                
                # Determine which normalization to apply based on CIDOC Type
                norm_name = ""
                if cidoc_type == 'E21 Person':
                    norm_name = normalize_person(raw_name)
                elif cidoc_type in ['E53 Place', 'E74 Group']:
                    norm_name = normalize_place_group(raw_name)
                else:
                    norm_name = normalize_work(raw_name)
                
                match_found = False
                match_info = None
                
                # 1. Try Normalized Match
                if norm_name in lookup:
                    match_found = True
                    match_info = lookup[norm_name][0] # Take first
                
                # 2. Fallback: Try Person normalization for Places (handling misclassification)
                # e.g. "Algarotti, Francesco" (Place) -> "Francesco Algarotti" (Person)
                if not match_found and cidoc_type == 'E53 Place':
                    alt_norm = normalize_person(raw_name)
                    if alt_norm in lookup:
                        match_found = True
                        match_info = lookup[alt_norm][0]
                        match_info['note'] = "Cross-Category Match"

                if match_found:
                    results['matches'] += 1
                    results['details'].append({
                        'Index_Entry': raw_name,
                        'CIDOC_Type': cidoc_type,
                        'Normalized_Key': norm_name,
                        'Matched_Name': match_info['original_name'],
                        'Matched_QID': match_info['qid'],
                        'Source_Table': match_info['source_file'],
                        'Note': match_info.get('note', 'Direct Match')
                    })
                else:
                    results['no_matches'] += 1
                    
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    return results

def main():
    base_dir = r'c:\Users\001\Desktop\Github-Project\PnPDataset'
    
    print("Loading Handmade Dataset (05) with Advanced Normalization...")
    lookup = load_handmade_data(base_dir)
    
    print("Comparing with Index Dataset (04)...")
    results = process_index_files(base_dir, lookup)
    
    # Generate Report
    report_path = os.path.join(base_dir, r'99-Python\02-Analysis\Advanced_Comparison_Report.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Advanced Data Comparison Report\n\n")
        f.write(f"**Total Entries:** {results['total_entries']}\n")
        f.write(f"**Matches Found:** {results['matches']} ({results['matches']/results['total_entries']*100:.1f}%)\n")
        f.write(f"**No Matches:** {results['no_matches']}\n\n")
        
        f.write("## Sample Matches (Advanced)\n")
        f.write("| Index Entry | Type | Normalized Key | Matched Name | QID | Note |\n")
        f.write("|---|---|---|---|---|---|\n")
        
        count = 0
        for item in results['details']:
            if count < 50:
                f.write(f"| {item['Index_Entry']} | {item['CIDOC_Type']} | {item['Normalized_Key']} | {item['Matched_Name']} | {item['Matched_QID']} | {item['Note']} |\n")
                count += 1
                
    print(f"Report generated at {report_path}")

if __name__ == "__main__":
    main()
