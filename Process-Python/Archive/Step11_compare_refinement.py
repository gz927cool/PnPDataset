import csv
import os

old_file = r"c:\Users\001\Desktop\list\04-Enrich\A.csv"
new_file = r"c:\Users\001\Desktop\list\07-Refined-A\A.csv"

def compare_files():
    print(f"Comparing Old (04-Enrich) vs New (07-Refined-A) for A.csv\n")
    
    old_data = {}
    with open(old_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            old_data[row['Main Entry']] = row['Type']
            
    new_data = {}
    with open(new_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_data[row['Main Entry']] = row['Type']
            
    # Find differences
    changes = []
    for entry, new_type in new_data.items():
        old_type = old_data.get(entry, "Unknown")
        if old_type != new_type:
            changes.append({
                'Entry': entry,
                'Old': old_type,
                'New': new_type
            })
            
    print(f"Total entries: {len(new_data)}")
    print(f"Total changes: {len(changes)}\n")
    
    if changes:
        print(f"{'Main Entry':<50} | {'Old Type':<15} | {'New Type':<15}")
        print("-" * 85)
        for c in changes:
            print(f"{c['Entry']:<50} | {c['Old']:<15} | {c['New']:<15}")

if __name__ == "__main__":
    compare_files()
