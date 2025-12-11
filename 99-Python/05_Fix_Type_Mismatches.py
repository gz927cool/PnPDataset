import os
import pandas as pd

enrich_dir = r"c:\Users\001\Desktop\list\04-Enrich"

# Updates based on the verification report
updates = {
    "Albani, Gianfrancesco (Pope Clement XI)": "E21 Person",
    "Castro, First and Second Wars of": "E5 Event",
    "Colonna, Prince Francesco": "E21 Person",
    "Flemish artists in Rome": "E74 Group",
    "Paris, Venetian 18th-century artists in": "E74 Group",
    "Religious orders, patronage by": "E28 Conceptual Object",
    "Spanish Succession, War of": "E5 Event",
    "'Status-seeking' by artists in 17th-century Rome": "E28 Conceptual Object",
    "Urbino, Francesco Maria della Rovere, Duke of": "E21 Person",
    "Wars of late 17th century, influence on art patronage": "E28 Conceptual Object"
}

def apply_fixes():
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
                
                # Check if term is wrapped in quotes (just in case)
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
    apply_fixes()
