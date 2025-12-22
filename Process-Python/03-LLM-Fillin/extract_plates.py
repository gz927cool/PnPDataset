import re
import csv
import os

def parse_plates(md_file_path, output_csv_path):
    with open(md_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    entries = []
    start_processing = False
    full_text = ""
    
    print(f"DEBUG: Total lines in file: {len(lines)}")
    
    for i, line in enumerate(lines):
        # Check for start condition
        # We look for "List of Plates" followed immediately (next line) by "PLATE FOLLOWING PAGE"
        if "List of Plates" in line:
            # Check next line safely
            if i + 1 < len(lines):
                next_line = lines[i+1].strip()
                if "PLATE FOLLOWING PAGE" in next_line:
                    start_processing = True
                    print(f"DEBUG: Found start at line {i}")
                    continue
        
        if start_processing and "Photographic Sources" in line:
            print(f"DEBUG: Found end at line {i}")
            break
        
        if start_processing:
            clean_line = line.strip()
            # Skip page headers/footers
            if clean_line.startswith("[Page") or clean_line.lower() == "plate following page" or not clean_line:
                continue
            full_text += clean_line + " "

    # Normalize spaces
    full_text = re.sub(r'\s+', ' ', full_text).strip()
    
    # Fix OCR specific issues mentioned
    full_text = full_text.replace("il a ", "11 a ")
    full_text = full_text.replace("I Valentin", "1 Valentin")
    # Fix { used as (
    full_text = full_text.replace("{", "(")
    
    # Fix stuck numbers and letters (e.g., "31a" -> "31 a")
    full_text = re.sub(r'(\d+)([a-z])\s', r'\1 \2 ', full_text)
    
    print(f"DEBUG: Text length: {len(full_text)}")
    if len(full_text) > 0:
        print(f"DEBUG: Text sample: {full_text[:100]} ...")

    # Insert delimiters
    # 1. Numbered Items: Space + Number + Space + (Optional Letter + Space) + Capital Letter ... + Colon
    # Added strict lookahead for Colon to avoid matching Page Numbers followed by Proper Nouns (e.g. "104 Beuningen")
    
    # Regex explanation:
    # (?:^|\s) -> Match start of string OR a space
    # (\d{1,2}) -> Group 1: Number (1 or 2 digits only, max 99, to avoid Page Numbers like 104, 200)
    # \s+ -> Space
    # ([a-z]\s+)? -> Group 2: Optional letter + space
    # (?=[A-Z][^:]+:) -> Lookahead for Capital Letter + text + Colon
    
    full_text = re.sub(r'(?:^|\s)(\d{1,2})\s+([a-z]\s+)?(?=[A-Z][^:]+:)', r'|||\1 \2', full_text)
    
    # 2. Sub Items: Space + Letter + Space + Capital Letter ... + Colon
    full_text = re.sub(r'(?:^|\s)([a-z])\s+(?=[A-Z][^:]+:)', r'|||\1 ', full_text)
    
    raw_items = full_text.split('|||')
    print(f"DEBUG: Found {len(raw_items)} raw items")
    
    current_num = ""
    
    for item in raw_items:
        item = item.strip()
        if not item:
            continue
            
        # Parse Item
        # Check if it starts with Number
        num_match = re.match(r'^(\d+)\s*([a-z])?\s*(.*)', item)
        sub_match = re.match(r'^([a-z])\s+(.*)', item)
        
        plate_id = ""
        sub_id = ""
        content = ""
        
        if num_match:
            current_num = num_match.group(1)
            sub_id = num_match.group(2) if num_match.group(2) else ""
            content = num_match.group(3)
            plate_id = current_num
        elif sub_match:
            plate_id = current_num
            sub_id = sub_match.group(1)
            content = sub_match.group(2)
        else:
            # Fallback for lines that didn't match start pattern but were split?
            # Or maybe just append to previous if it's not a new item?
            # But we split by ||| which denotes new item.
            # If regex failed to identify it as new item, it's part of previous text.
            pass

        if content and ":" in content:
            parts = content.split(":", 1)
            artist = parts[0].strip()
            desc = parts[1].strip()
            
            # Clean description (remove page numbers at end)
            # Remove trailing digits
            desc = re.sub(r'\s+\d+$', '', desc)
            
            # Extract Location if in parentheses at end
            location = ""
            # Regex for location: (Location text) at end of string
            # Be careful of nested parens or multiple parens. Usually location is last.
            loc_match = re.search(r'\(([^)]+)\)$', desc)
            if loc_match:
                location = loc_match.group(1)
                desc = desc[:loc_match.start()].strip()
            
            entries.append({
                "Plate_ID": plate_id,
                "Sub_ID": sub_id,
                "Artist": artist,
                "Title_Description": desc,
                "Location": location
            })
        else:
            # Handle cases without colon? (rare in this dataset based on preview)
            pass

    # Write to CSV
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Plate_ID', 'Sub_ID', 'Artist', 'Title_Description', 'Location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for e in entries:
            writer.writerow(e)

if __name__ == "__main__":
    md_path = r"c:\Users\001\Desktop\Github-Project\PnPDataset\02-Markdown\00_05_List_of_Plates.md"
    csv_path = r"c:\Users\001\Desktop\Github-Project\PnPDataset\Worklist-index\Worklist_Plates.csv"
    parse_plates(md_path, csv_path)
    print(f"Extraction complete. Saved to {csv_path}")
