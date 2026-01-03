import pandas as pd
import os

# Define paths
base_dir = r"c:\Users\001\Desktop\Github-Project\PnPDataset"
corrected_file = os.path.join(base_dir, r"09-MissingQID-LLM-Fillin\07-Human-Merge\06-Requery_Filled_Human_Merged_Corrected.csv")
worklist_file = os.path.join(base_dir, r"10-Worklist-index\Worklist_Plates.csv")
output_file = os.path.join(base_dir, r"10-Worklist-index\Worklist_Plates_Matched.csv")

import difflib

print(f"Loading QID source: {corrected_file}")
df_qid = pd.read_csv(corrected_file)

print(f"Loading Worklist: {worklist_file}")
df_work = pd.read_csv(worklist_file)

# Create Lookup Dictionary
# Key: Refined_Formal_Name, Value: Original-QID
df_qid_clean = df_qid.dropna(subset=['Original-QID'])
# Normalize keys to lower case for easier matching
name_to_qid = dict(zip(df_qid_clean['Refined_Formal_Name'].str.strip(), df_qid_clean['Original-QID'].astype(str).str.strip()))
# Also create a lower-case map for case-insensitive lookup
name_to_qid_lower = {k.lower(): v for k, v in name_to_qid.items()}
# List of known names for fuzzy matching
known_names = list(name_to_qid.keys())
known_names_lower = [n.lower() for n in known_names]

print(f"Loaded {len(name_to_qid)} QID mappings.")

# Manual Mapping for known abbreviations or variations in Worklist
manual_map = {
    "Velasquez": "Diego Velázquez",
    "G. M. Crespi": "Giuseppe Maria Crespi (Lo Spagnuolo)",
    "A. D. Gabbiani": "Anton Domenico Gabbiani",
    "G. Volpato": "Giovanni Volpato",
    "Marco Ricci (engraved Bartolozzi)": "Marco Ricci",
    "Tiepolo (engraved Leonardis)": "Giovanni Battista Tiepolo",
    "Mola and Simonelli": "Pier Francesco Mola",
    "Canaletto, Cimaroli and Pittoni": "Canaletto",
    "Gio. Maria Bottalla": "Giovanni Maria Bottala (Raffaellino)", # Ensure this maps if fuzzy fails
    "P. Van Bleek": "Peter van Bleeck"
}

# Track fuzzy matches for reporting
fuzzy_matches_log = []

# Helper function
def get_qid(name):
    if pd.isna(name) or str(name).strip() == '':
        return ''
    
    target = str(name).strip()
    
    # 0. Manual Map
    if target in manual_map:
        mapped_name = manual_map[target]
        if mapped_name in name_to_qid:
            return name_to_qid[mapped_name]
            
    target_lower = target.lower()
    
    # 1. Exact Match
    if target in name_to_qid:
        return name_to_qid[target]
        
    # 2. Case-insensitive Match
    if target_lower in name_to_qid_lower:
        return name_to_qid_lower[target_lower]
    
    # 3. Substring / Token Match (The "Fuzzy" part)
    # We look for the target being a substring of a known name
    # e.g. "Bernini" in "Gian Lorenzo Bernini"
    candidates = []
    for idx, known in enumerate(known_names_lower):
        if target_lower in known:
            candidates.append(known_names[idx])
            
    if candidates:
        # Heuristic: Pick the shortest match that contains the target
        # This avoids matching "Rome" to "Allegory of Rome" if "Rome" exists (handled by exact match),
        # but if "Rome" doesn't exist, "Allegory of Rome" might be wrong for Location "Rome".
        # However, for Artists like "Bernini", shortest containing string "Gian Lorenzo Bernini" is likely correct.
        best_match = min(candidates, key=len)
        
        # Log it
        fuzzy_matches_log.append(f"'{target}' -> '{best_match}' (Substring)")
        return name_to_qid[best_match]
        
    # 4. Difflib Close Match (for typos)
    # cutoff=0.8 means 80% similarity
    matches = difflib.get_close_matches(target, known_names, n=1, cutoff=0.8)
    if matches:
        best_match = matches[0]
        fuzzy_matches_log.append(f"'{target}' -> '{best_match}' (Similarity)")
        return name_to_qid[best_match]

    return ''

# Insert Columns
# Note: insert modifies dataframe in place.
# Columns: Plate_ID, Sub_ID, Artist, Title_Description, Location
# Indices: 0,        1,      2,      3,                 4

print("Matching Artists (with fuzzy logic)...")
# Insert Artist_QID after Artist (index 2 -> insert at 3)
artist_qids = df_work['Artist'].apply(get_qid)
df_work.insert(3, 'Artist_QID', artist_qids)
print(f"  Matched {len(artist_qids[artist_qids != ''])} / {len(df_work)} Artists")

print("Matching Titles (with fuzzy logic)...")
# Title_Description is now at index 4 (was 3). Insert Title_QID at 5.
title_qids = df_work['Title_Description'].apply(get_qid)
df_work.insert(5, 'Title_QID', title_qids)
print(f"  Matched {len(title_qids[title_qids != ''])} / {len(df_work)} Titles")

print("Matching Locations (with fuzzy logic)...")
# Location is now at index 6 (was 4). Insert Location_QID at 7.
location_qids = df_work['Location'].apply(get_qid)
df_work.insert(7, 'Location_QID', location_qids)
print(f"  Matched {len(location_qids[location_qids != ''])} / {len(df_work)} Locations")

# Save
df_work.to_csv(output_file, index=False)
print("-" * 30)
print(f"Saved matched worklist to: {output_file}")

# Report Fuzzy Matches
print("\nSample of Fuzzy Matches Applied:")
# Deduplicate log
unique_log = list(set(fuzzy_matches_log))
for log in unique_log[:20]:
    print(f"  {log}")

# Report on missing matches for first few rows
print("\nSample of missing matches (Artist):")
missing_artists = df_work[df_work['Artist_QID'] == '']['Artist'].unique()
print(missing_artists[:10])

