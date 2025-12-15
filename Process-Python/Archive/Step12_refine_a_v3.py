import csv
import os
import re

input_file = r"c:\Users\001\Desktop\list\04-Enrich\A.csv"
output_file = r"c:\Users\001\Desktop\list\07-Refined-A\A_v2.csv"

def refine_classification_v2(row):
    entry = row.get('Main Entry', '').strip()
    entry_lower = entry.lower()
    
    # 1. Explicit Overrides (Specific Concepts or Persons that might be ambiguous)
    if "artistic temperament" in entry_lower: return "Concept"
    if "artist's position" in entry_lower: return "Concept"
    if "artists, status of" in entry_lower: return "Concept"
    if "anti-papal satire" in entry_lower: return "Concept"
    if "art dealers" in entry_lower: return "Group"
    
    if entry_lower in ["alexander vii", "alexander viii", "ariosto", "arrighini"]:
        return "Person"
        
    # 2. Event (Higher priority to prevent "Peace of ... Chapelle" being caught as Architecture)
    if "exhibitions" in entry_lower: return "Event"
    if any(x in entry_lower for x in ['peace of', 'treaty of', 'council of', 'battle of', 'sack of']):
        return "Event"

    # 3. Architecture (New Category)
    # Specific buildings, villas, palaces
    # Note: "Church" can be a surname, but usually "Church of..." or "S. ..." handles buildings.
    # We check for specific architectural terms.
    if any(x in entry_lower for x in ['palazzo', 'palace', 'villa', 'cathedral', 'basilica', 'chapel', 'temple', 'alticchiero']):
        return "Architecture"
    
    # "Church" needs care to avoid "Frederic Church" (Person). 
    # If it starts with "Church", it's likely "Church of...". 
    # If it contains "church" and no comma, likely architecture.
    if 'church' in entry_lower:
        if ',' not in entry:
            return "Architecture"
    
    # San/Santa/S. usually denotes a church if it's a Main Entry and not a person
    if entry_lower.startswith(('san ', 'santa ', 's. ')):
        if ',' not in entry:
            return "Architecture"

    # 4. Place (Generic Locations)
    # Cities, regions, squares, streets
    if any(x in entry_lower for x in ['piazza', 'square', 'street', 'garden', 'park', 'rome', 'venice', 'florence']):
        return "Place"

    # 5. Institution
    if any(x in entry_lower for x in ['accademia', 'academy', 'society', 'college', 'university', 'school', 'scuola']):
        return "Institution"

    # 6. Person
    # Default assumption: Comma usually implies "Surname, Firstname"
    if ',' in entry:
        if not any(x in entry_lower for x in ['status of', 'development of']):
            return "Person"

    # 7. Fallback
    return "Subject"

def process_a_v2():
    print(f"Refining {input_file} with Architecture category (v2.1)...")
    
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))

    with open(input_file, 'r', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames
        
        rows = []
        for row in reader:
            new_type = refine_classification_v2(row)
            row['Type'] = new_type
            rows.append(row)
            
    with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Saved refined file to {output_file}")
    
    # Verification
    print("\n--- Verification of Key Entries ---")
    targets = ["Alticchiero", "Altieri palace", "Aix-la-Chapelle", "San Giovanni"]
    
    for r in rows:
        entry = r['Main Entry']
        # Check if this entry matches any of our targets (partial match)
        if any(t.lower() in entry.lower() for t in targets):
            print(f"  [{r['Type']}] {entry}")

if __name__ == "__main__":
    process_a_v2()
