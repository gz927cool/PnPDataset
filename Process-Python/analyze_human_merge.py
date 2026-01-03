import csv
import os
from collections import Counter

file_path = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\07-Human-Merge\01-Requery_Filled_Human_Merged.csv"

def analyze_csv(file_path):
    print(f"Analyzing file: {file_path}")
    
    total_rows = 0
    filled_qid_count = 0
    missing_qid_count = 0
    names = []
    categories = []
    
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        print(f"Columns: {fieldnames}")
        
        for row in reader:
            total_rows += 1
            
            # Check QID
            qid = row.get('Original-QID', '').strip()
            if qid:
                filled_qid_count += 1
            else:
                missing_qid_count += 1
            
            # Collect Names for duplicate check
            name = row.get('Refined_Formal_Name', '').strip()
            if name:
                names.append(name)
                
            # Collect Category if exists
            # Note: Column name might vary, checking common ones
            cat = row.get('Refined_Category') or row.get('Original-Refined_Category') or row.get('Entity_Type')
            if cat:
                categories.append(cat)

    # Duplicate Analysis
    name_counts = Counter(names)
    duplicates = {k: v for k, v in name_counts.items() if v > 1}
    
    # Category Analysis
    cat_counts = Counter(categories)

    print("-" * 30)
    print("DATASET STATISTICS")
    print("-" * 30)
    print(f"Total Rows: {total_rows}")
    print(f"Rows with QID: {filled_qid_count} ({filled_qid_count/total_rows*100:.1f}%)")
    print(f"Rows MISSING QID: {missing_qid_count} ({missing_qid_count/total_rows*100:.1f}%)")
    
    print("-" * 30)
    print(f"Duplicate Names Found: {len(duplicates)}")
    if duplicates:
        print("Top 10 Duplicates:")
        for name, count in list(duplicates.items())[:10]:
            print(f"  - {name}: {count} times")
            
    print("-" * 30)
    print("Category Distribution (Top 5):")
    for cat, count in cat_counts.most_common(5):
        print(f"  - {cat}: {count}")

if __name__ == "__main__":
    if os.path.exists(file_path):
        analyze_csv(file_path)
    else:
        print(f"File not found: {file_path}")
