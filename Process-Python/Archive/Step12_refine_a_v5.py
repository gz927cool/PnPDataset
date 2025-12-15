import csv
import os
import re

input_file = r"c:\Users\001\Desktop\list\04-Enrich\A.csv"
output_file = r"c:\Users\001\Desktop\list\07-Refined-A\A_v2.csv"

def refine_classification_v5(row):
    entry = row.get('Main Entry', '').strip()
    entry_lower = entry.lower()
    
    # --- 1. Explicit Overrides ---
    if "artistic temperament" in entry_lower: return "Concept"
    if "artist's position" in entry_lower: return "Concept"
    if "artists, status of" in entry_lower: return "Concept"
    if "anti-papal satire" in entry_lower: return "Concept"
    
    if entry_lower in ["alexander vii", "alexander viii", "ariosto", "arrighini"]:
        return "Person"

    # --- 2. Specific Entity Types (High Priority) ---

    # Treaty / Legal Agreement
    if any(x in entry_lower for x in ['peace of', 'treaty of', 'truce of', 'concordat of', 'armistice of']):
        return "Treaty"

    # Literature / Artworks (Books, Poems, Paintings as Main Entry)
    # Add known titles here if they appear as Main Entry
    if entry_lower in ['daphnis and chloe', 'orlando furioso', 'divine comedy', 'the prince']:
        return "Literature"

    # Family
    if 'family' in entry_lower:
        return "Family"

    # Group / Organization (Non-Institution)
    if any(x in entry_lower for x in ['dealers', 'painters', 'sculptors', 'architects', 'bamboccianti', 'dominicans', 'jesuits', 'franciscans']):
        return "Group"

    # Event
    if "exhibitions" in entry_lower: return "Event"
    if any(x in entry_lower for x in ['council of', 'battle of', 'sack of', 'siege of', 'synod of']):
        return "Event"

    # Architecture
    # Specific buildings, villas, palaces
    if any(x in entry_lower for x in ['palazzo', 'palace', 'villa', 'cathedral', 'basilica', 'chapel', 'temple', 'alticchiero']):
        return "Architecture"
    
    if 'church' in entry_lower:
        if ',' not in entry:
            return "Architecture"
    
    if entry_lower.startswith(('san ', 'santa ', 's. ')):
        if ',' not in entry:
            return "Architecture"

    # Institution
    if any(x in entry_lower for x in ['accademia', 'academy', 'society', 'college', 'university', 'school', 'scuola']):
        return "Institution"

    # Place (Generic Locations)
    if any(x in entry_lower for x in ['piazza', 'square', 'street', 'garden', 'park', 'rome', 'venice', 'florence', 'naples', 'bologna', 'milan', 'paris', 'london']):
        return "Place"

    # --- 3. Person (Default for Name-like patterns) ---
    # Comma usually implies "Surname, Firstname"
    if ',' in entry:
        # Exclude things that might have commas but aren't people
        if not any(x in entry_lower for x in ['status of', 'development of', 'peace of', 'treaty of']):
            return "Person"

    # --- 4. Fallback ---
    return "Subject"

def process_a_v5():
    print(f"Refining {input_file} with Expanded Taxonomy (v5)...")
    
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))

    with open(input_file, 'r', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames
        
        rows = []
        for row in reader:
            new_type = refine_classification_v5(row)
            row['Type'] = new_type
            rows.append(row)
            
    with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Saved refined file to {output_file}")
    
    # Verification
    print("\n--- Verification of Categories ---")
    
    # Count types
    from collections import Counter
    types = [r['Type'] for r in rows]
    counts = Counter(types)
    for t, c in counts.most_common():
        print(f"  {t}: {c}")

    print("\n--- Key Examples ---")
    targets = ["Alticchiero", "Altieri palace", "Aix-la-Chapelle", "Art dealers", "Art exhibitions", "Anti-papal satire"]
    for r in rows:
        if any(t.lower() in r['Main Entry'].lower() for t in targets):
            print(f"  [{r['Type']}] {r['Main Entry']}")

if __name__ == "__main__":
    process_a_v5()
