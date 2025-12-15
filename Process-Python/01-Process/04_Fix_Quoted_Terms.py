import os
import pandas as pd

enrich_dir = r"c:\Users\001\Desktop\list\04-Enrich"

# Handle the remaining stubborn unknowns
updates = {
    "'Baciccio'": "E21 Person",
    "'Rosichino'": "E21 Person",
    "Baciccio": "E21 Person",
    "Rosichino": "E21 Person"
}

def fix_remaining():
    files = [f for f in os.listdir(enrich_dir) if f.endswith(".csv")]
    total_updated = 0
    
    for filename in files:
        path = os.path.join(enrich_dir, filename)
        try:
            df = pd.read_csv(path)
            if 'Main Entry' not in df.columns or 'Type' not in df.columns:
                continue
                
            updated_in_file = 0
            
            for index, row in df.iterrows():
                term = row['Main Entry']
                current_type = str(row['Type']).strip()
                
                # Check exact match
                if term in updates:
                    if current_type != updates[term]:
                        df.at[index, 'Type'] = updates[term]
                        updated_in_file += 1
                
                # Check if term is wrapped in quotes
                clean_term = term.strip("'")
                if clean_term in updates:
                     if current_type != updates[clean_term]:
                        df.at[index, 'Type'] = updates[clean_term]
                        updated_in_file += 1

            if updated_in_file > 0:
                df.to_csv(path, index=False, encoding='utf-8-sig')
                print(f"Updated {updated_in_file} entries in {filename}")
                total_updated += updated_in_file
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    print(f"Total updates applied: {total_updated}")

if __name__ == "__main__":
    fix_remaining()
