import csv
import os
import re

input_file = r"c:\Users\001\Desktop\list\04-Enrich\A.csv"
output_file = r"c:\Users\001\Desktop\list\07-Refined-A\A_v2.csv"

def refine_classification_v4(row):
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

    # 2. Treaty (New Category - Specific User Request)
    # Must come before Event
    if any(x in entry_lower for x in ['peace of', 'treaty of', 'truce of', 'concordat of', 'armistice of']):
        return "Treaty"
        
    # 3. Event
    if "exhibitions" in entry_lower: return "Event"
    if any(x in entry_lower for x in ['council of', 'battle of', 'sack of', 'siege of']):
        return "Event"

    # 4. Architecture
    # Specific buildings, villas, palaces
    if any(x in entry_lower for x in ['palazzo', 'palace', 'villa', 'cathedral', 'basilica', 'chapel', 'temple', 'alticchiero']):
        return "Architecture"
    
    if 'church' in entry_lower:
        if ',' not in entry:
            return "Architecture"
    
    if entry_lower.startswith(('san ', 'santa ', 's. ')):
        if ',' not in entry:
            return "Architecture"

    # 5. Place (Generic Locations)
    if any(x in entry_lower for x in ['piazza', 'square', 'street', 'garden', 'park', 'rome', 'venice', 'florence']):
        return "Place"

    # 6. Institution
    if any(x in entry_lower for x in ['accademia', 'academy', 'society', 'college', 'university', 'school', 'scuola']):
        return "Institution"

    # 7. Person
    if ',' in entry:
        if not any(x in entry_lower for x in ['status of', 'development of']):
            return "Person"

    # 8. Fallback
    return "Subject"

def process_a_v4():
    print(f"Refining {input_file} with Treaty category (v4)...")
    
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))

    with open(input_file, 'r', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames
        
        rows = []
        for row in reader:
            new_type = refine_classification_v4(row)
            row['Type'] = new_type
            rows.append(row)
            
    with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Saved refined file to {output_file}")
    
    # Verification
    print("\n--- Verification of Key Entries ---")
    targets = ["Alticchiero", "Altieri palace", "Aix-la-Chapelle"]
    
    for r in rows:
        entry = r['Main Entry']
        if any(t.lower() in entry.lower() for t in targets):
            print(f"  [{r['Type']}] {entry}")

if __name__ == "__main__":
    process_a_v4()
