import csv
import os
import re

input_file = r"c:\Users\001\Desktop\list\04-Enrich\A.csv"
output_file = r"c:\Users\001\Desktop\list\07-Refined-A\A.csv"

def refine_classification(row):
    entry = row.get('Main Entry', '').strip()
    entry_lower = entry.lower()
    
    # 1. Explicit Overrides (Fixing previous misclassifications)
    if "artistic temperament" in entry_lower: return "Concept"
    if "artist's position" in entry_lower: return "Concept"
    if "artists, status of" in entry_lower: return "Concept"
    if "anti-papal satire" in entry_lower: return "Concept"
    if "art dealers" in entry_lower: return "Group" # Or Concept
    
    if entry_lower in ["alexander vii", "alexander viii", "ariosto", "arrighini"]:
        return "Person"
        
    if "alticchiero" in entry_lower: return "Place"
    if "altieri palace" in entry_lower: return "Place"
    
    # 2. Event Logic
    if "exhibitions" in entry_lower: return "Event"
    if any(x in entry_lower for x in ['peace of', 'treaty of', 'council of', 'battle of']):
        return "Event"

    # 3. Institution Logic
    if any(x in entry_lower for x in ['accademia', 'academy', 'society', 'college', 'university', 'school', 'scuola']):
        return "Institution"

    # 4. Place Logic
    if any(x in entry_lower for x in ['palazzo', 'villa', 'church', 'cathedral', 'basilica']):
        return "Place"
    # Check for San/Santa at start, but exclude names like "San Giovanni, Giovanni da" (which has comma)
    if entry_lower.startswith(('san ', 'santa ', 's. ')):
        if ',' not in entry:
            return "Place"

    # 5. Person Logic
    # Most names have a comma: "Surname, Name"
    if ',' in entry:
        # Exclude non-person phrases with commas
        if not any(x in entry_lower for x in ['peace of', 'treaty of', 'status of', 'development of']):
            return "Person"

    # 6. Fallback
    return "Subject"

def process_a():
    print(f"Refining {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames
        
        rows = []
        for row in reader:
            new_type = refine_classification(row)
            row['Type'] = new_type
            rows.append(row)
            
    with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Saved refined file to {output_file}")

if __name__ == "__main__":
    process_a()
