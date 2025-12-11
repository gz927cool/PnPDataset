import csv
import os
import re

source_dir = r"c:\Users\001\Desktop\list\03-CSV"
output_dir = r"c:\Users\001\Desktop\list\05-Classified-CSV"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def classify_entry(entry):
    entry_lower = entry.lower()
    
    # Institutions
    if any(x in entry_lower for x in ['accademia', 'academy', 'society', 'college', 'university', 'school', 'scuola', 'guild']):
        return 'Institution'
    
    # Places / Buildings
    if any(x in entry_lower for x in ['palazzo', 'villa', 'church', 'cathedral', 'basilica', 'san ', 'santa ', 's. ']):
        # Be careful with "San" in names, but usually names are "Surname, Name"
        # If it starts with these, it's likely a place
        if entry_lower.startswith(('palazzo', 'villa', 'church', 'cathedral', 'basilica', 'san ', 'santa ', 's. ')):
            return 'Place'
            
    # Events
    if any(x in entry_lower for x in ['peace of', 'treaty of', 'council of', 'battle of', 'siege of']):
        return 'Event'
        
    # Persons
    # Pattern: Word, Word (Surname, Name)
    # Exclude things like "Aix-la-Chapelle, Peace of" which is caught above
    if ',' in entry:
        # Check if it looks like a name
        parts = entry.split(',')
        if len(parts) >= 2:
            return 'Person'
            
    # Subjects / Concepts / Groups
    # Default fallback
    return 'Subject'

def process_files():
    csv_files = [f for f in os.listdir(source_dir) if f.endswith('.csv')]
    
    for filename in csv_files:
        print(f"Processing {filename}...")
        input_path = os.path.join(source_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        # Try different encodings
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
        content = None
        used_encoding = None
        
        for enc in encodings:
            try:
                with open(input_path, 'r', encoding=enc) as f:
                    content = f.read()
                    used_encoding = enc
                    break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"Failed to read {filename} with supported encodings.")
            continue
            
        print(f"  Read with encoding: {used_encoding}")
        
        # Parse content
        from io import StringIO
        f_in = StringIO(content)
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames
        
        if not fieldnames:
            print(f"  Warning: No fields found in {filename}")
            continue

        # Insert 'Type' after 'Main Entry'
        if 'Type' not in fieldnames:
            if 'Main Entry' in fieldnames:
                main_entry_index = fieldnames.index('Main Entry')
                new_fieldnames = fieldnames[:main_entry_index+1] + ['Type'] + fieldnames[main_entry_index+1:]
            else:
                new_fieldnames = ['Type'] + fieldnames
        else:
            new_fieldnames = fieldnames
            
        rows = []
        for row in reader:
            main_entry = row.get('Main Entry', '')
            entry_type = classify_entry(main_entry)
            row['Type'] = entry_type
            rows.append(row)
            
        with open(output_path, 'w', encoding='utf-8', newline='') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=new_fieldnames)
            writer.writeheader()
            writer.writerows(rows)
            
    print(f"Done. Classified files saved to {output_dir}")

if __name__ == "__main__":
    process_files()
