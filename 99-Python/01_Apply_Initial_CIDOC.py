import csv
import os
import glob
import re

# Configuration
source_dir = r"c:\Users\001\Desktop\list\03-CSV"
target_dir = r"c:\Users\001\Desktop\list\04-Enrich"

# CIDOC-CRM Constants
TYPE_PERSON = "E21 Person"
TYPE_GROUP = "E74 Group"
TYPE_EVENT = "E5 Event"
TYPE_MAN_MADE = "E22 Man-Made Object"
TYPE_CONCEPT = "E28 Conceptual Object"
TYPE_PLACE = "E53 Place"
TYPE_UNKNOWN = "Unknown"

def analyze_and_classify(row):
    """
    Performs deep content analysis on the Main Entry and context columns
    to assign a CIDOC-CRM category.
    """
    main_entry = row.get('Main Entry', '').strip()
    sub_entry = row.get('Sub-entry', '').strip()
    detail = row.get('Detail', '').strip()
    
    entry_lower = main_entry.lower()
    
    # --- 1. E28 Conceptual Object (Concepts, Theories) ---
    # High priority for abstract concepts
    concept_keywords = [
        "artistic temperament", "artist's position", "status of", 
        "satire", "theory", "criticism", "development of", "concept of",
        "allegory", "iconography"
    ]
    if any(kw in entry_lower for kw in concept_keywords):
        return TYPE_CONCEPT

    # --- 2. E5 Event (Events, Treaties, Exhibitions) ---
    event_keywords = [
        "peace of", "treaty of", "council of", "battle of", "sack of", 
        "synod of", "concordat of", "armistice of", "exhibitions",
        "entry of", "ceremony", "festival", "carnival"
    ]
    if any(kw in entry_lower for kw in event_keywords):
        return TYPE_EVENT

    # --- 3. E74 Group (Institutions, Families, Organizations) ---
    group_keywords = [
        "family", "accademia", "academy", "society", "college", 
        "university", "school", "scuola", "dealers", "painters", 
        "sculptors", "architects", "bamboccianti", "dominicans", 
        "jesuits", "franciscans", "order of", "guild"
    ]
    if any(kw in entry_lower for kw in group_keywords):
        return TYPE_GROUP

    # --- 4. E22 Man-Made Object (Architecture, Artworks, Books) ---
    # Architecture
    arch_keywords = [
        "palazzo", "palace", "villa", "cathedral", "basilica", 
        "chapel", "temple", "alticchiero", "church", "monument", 
        "fountain", "arch", "bridge", "castle"
    ]
    if any(kw in entry_lower for kw in arch_keywords):
        return TYPE_MAN_MADE
    
    # Specific check for "S. " or "San " which usually means a church if not a person
    # If it has a comma, it's likely a person (e.g. "San Giovanni, Giovanni da")
    if (entry_lower.startswith('s. ') or entry_lower.startswith('san ') or entry_lower.startswith('santa ')) and ',' not in main_entry:
        return TYPE_MAN_MADE

    # Literature / Specific Works (if they appear as Main Entry)
    lit_keywords = ["orlando furioso", "divine comedy", "the prince", "lives of the artists", "daphnis and chloe"]
    if entry_lower in lit_keywords:
        # Literature can be E28 (Content) or E22 (Book). 
        # In art history context, usually referring to the text/story -> E28.
        # But user asked for "Man-Made Object" for buildings. 
        # Let's stick to E28 for Literature to distinguish from Buildings.
        return TYPE_CONCEPT 

    # --- 5. E53 Place (Geographic Locations) ---
    place_keywords = [
        "piazza", "square", "street", "garden", "park", "rome", 
        "venice", "florence", "naples", "bologna", "milan", "paris", 
        "london", "vatican", "holland", "flanders", "spain", "france"
    ]
    if any(kw in entry_lower for kw in place_keywords):
        return TYPE_PLACE

    # --- 6. E21 Person (People) ---
    # Default heuristic: Comma implies "Surname, Firstname"
    # Must be checked AFTER Events/Concepts which might contain commas (e.g. "Aix-la-Chapelle, Peace of")
    if ',' in main_entry:
        return TYPE_PERSON
    
    # Known single names or Popes
    person_keywords = ["pope", "cardinal", "king", "queen", "duke", "duchess", "prince", "princess"]
    # But be careful, "Prince of Wales" is a person, "Prince" might be part of a title.
    # Specific overrides
    if entry_lower in ["alexander vii", "alexander viii", "ariosto", "arrighini", "baciccio", "canaletto", "dante", "giorgione", "guercino", "michelangelo", "raphael", "titian", "tintoretto", "veronese"]:
        return TYPE_PERSON

    # --- 7. Fallback ---
    # If we can't determine, default to Unknown or Subject
    return TYPE_UNKNOWN

def process_all_files():
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    csv_files = glob.glob(os.path.join(source_dir, "*.csv"))
    
    print(f"Found {len(csv_files)} files to process.")
    
    total_stats = {}
    
    for file_path in csv_files:
        filename = os.path.basename(file_path)
        output_path = os.path.join(target_dir, filename)
        
        print(f"Processing {filename}...")
        
        # Try reading with different encodings
        encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
        rows = []
        fieldnames = []
        
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc) as f_in:
                    reader = csv.DictReader(f_in)
                    fieldnames = reader.fieldnames
                    rows = list(reader) # Read all rows to check for encoding errors
                print(f"Successfully read {filename} with encoding: {enc}")
                break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Error reading {filename} with {enc}: {e}")
                continue
        
        if not rows:
            print(f"Failed to read {filename} with any supported encoding.")
            continue

        # Ensure 'Type' is in fieldnames, insert it after 'Main Entry' if possible
        if fieldnames and 'Type' not in fieldnames:
            new_fieldnames = ['Main Entry', 'Type'] + [f for f in fieldnames if f != 'Main Entry']
        else:
            new_fieldnames = fieldnames
        
        processed_rows = []
        for row in rows:
            cidoc_type = analyze_and_classify(row)
            row['Type'] = cidoc_type
            processed_rows.append(row)
            
            # Stats
            total_stats[cidoc_type] = total_stats.get(cidoc_type, 0) + 1
            
        with open(output_path, 'w', encoding='utf-8', newline='') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=new_fieldnames)
            writer.writeheader()
            writer.writerows(processed_rows)
            
    print("\nProcessing Complete.")
    print("Global Classification Statistics:")
    for k, v in sorted(total_stats.items()):
        print(f"  {k}: {v}")

if __name__ == "__main__":
    process_all_files()
