import csv
import os
import re

source_dir = r"c:\Users\001\Desktop\list\04-Enrich"

def check_places():
    csv_files = [f for f in os.listdir(source_dir) if f.endswith('.csv')]
    
    all_places = []
    
    print(f"Checking 'Place' entries in {len(csv_files)} files...\n")
    
    for filename in csv_files:
        filepath = os.path.join(source_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row_num, row in enumerate(reader, 1):
                    if row.get('Type') == 'Place':
                        all_places.append({
                            'File': filename,
                            'Line': row_num,
                            'Main Entry': row.get('Main Entry', ''),
                            'Location': row.get('Location', ''),
                            'Sub-entry': row.get('Sub-entry', ''),
                            'Detail': row.get('Detail', '')
                        })
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    print(f"Total 'Place' entries found: {len(all_places)}")
    
    if not all_places:
        return

    # Analysis 1: Missing Location
    missing_loc = [p for p in all_places if not p['Location'].strip()]
    print(f"\n[Issue 1] Places with missing 'Location' field: {len(missing_loc)}")
    if missing_loc:
        print("  Examples:")
        for p in missing_loc[:5]:
            print(f"    - {p['File']} (L{p['Line']}): {p['Main Entry']}")

    # Analysis 2: Naming Convention (Prefixes)
    prefixes = {}
    for p in all_places:
        entry = p['Main Entry'].strip()
        first_word = entry.split(' ')[0].lower() if ' ' in entry else entry.lower()
        prefixes[first_word] = prefixes.get(first_word, 0) + 1
        
    print(f"\n[Analysis 2] Common Prefixes for Places:")
    sorted_prefixes = sorted(prefixes.items(), key=lambda x: x[1], reverse=True)
    for prefix, count in sorted_prefixes[:10]:
        print(f"    - {prefix}: {count}")

    # Analysis 3: Potential Formatting Issues (e.g. trailing commas, weird characters)
    formatting_issues = []
    for p in all_places:
        entry = p['Main Entry']
        if entry.strip().endswith(','):
            formatting_issues.append((p, "Ends with comma"))
        if "  " in entry:
            formatting_issues.append((p, "Double spaces"))
        if entry.startswith('"') and not entry.endswith('"'):
             formatting_issues.append((p, "Unbalanced quotes"))

    print(f"\n[Issue 3] Potential Formatting Issues: {len(formatting_issues)}")
    if formatting_issues:
        for p, issue in formatting_issues[:10]:
             print(f"    - {p['File']} (L{p['Line']}): '{p['Main Entry']}' -> {issue}")

if __name__ == "__main__":
    check_places()
