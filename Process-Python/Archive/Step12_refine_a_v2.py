import csv
import os
import re

input_file = r"c:\Users\001\Desktop\list\04-Enrich\A.csv"
output_file = r"c:\Users\001\Desktop\list\07-Refined-A\A_v2.csv"

def refine_classification_v2(row):
    entry = row.get('Main Entry', '').strip()
    entry_lower = entry.lower()
    
    # 1. Explicit Overrides
    if "artistic temperament" in entry_lower: return "Concept"
    if "artist's position" in entry_lower: return "Concept"
    if "artists, status of" in entry_lower: return "Concept"
    if "anti-papal satire" in entry_lower: return "Concept"
    if "art dealers" in entry_lower: return "Group"
    
    if entry_lower in ["alexander vii", "alexander viii", "ariosto", "arrighini"]:
        return "Person"
        
    # 2. Architecture (New Category)
    # Specific buildings, villas, palaces
    if any(x in entry_lower for x in ['palazzo', 'palace', 'villa', 'church', 'cathedral', 'basilica', 'chapel', 'temple', 'alticchiero']):
        return "Architecture"
    
    # San/Santa/S. usually denotes a church if it's a Main Entry and not a person
    if entry_lower.startswith(('san ', 'santa ', 's. ')):
        if ',' not in entry:
            return "Architecture"

    # 3. Place (Generic Locations)
    # Cities, regions, squares, streets
    if any(x in entry_lower for x in ['piazza', 'square', 'street', 'garden', 'park', 'rome', 'venice', 'florence']):
        return "Place"

    # 4. Event
    if "exhibitions" in entry_lower: return "Event"
    if any(x in entry_lower for x in ['peace of', 'treaty of', 'council of', 'battle of']):
        return "Event"

    # 5. Institution
    if any(x in entry_lower for x in ['accademia', 'academy', 'society', 'college', 'university', 'school', 'scuola']):
        return "Institution"

    # 6. Person
    if ',' in entry:
        if not any(x in entry_lower for x in ['peace of', 'treaty of', 'status of', 'development of']):
            return "Person"

    # 7. Fallback
    return "Subject"

def process_a_v2():
    print(f"Refining {input_file} with Architecture category...")
    
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
    
    # Compare with v1 (or original)
    print("\n--- Comparison with previous classification (Place vs Architecture) ---")
    # Let's compare with the 'Place' logic from v1
    # In v1, Alticchiero was 'Place'. In v2, it should be 'Architecture'.
    
    count_arch = 0
    count_place = 0
    for r in rows:
        if r['Type'] == 'Architecture':
            print(f"  [Architecture] {r['Main Entry']}")
            count_arch += 1
        elif r['Type'] == 'Place':
            print(f"  [Place] {r['Main Entry']}")
            count_place += 1
            
    print(f"\nTotal Architecture: {count_arch}")
    print(f"Total Place: {count_place}")

if __name__ == "__main__":
    process_a_v2()
