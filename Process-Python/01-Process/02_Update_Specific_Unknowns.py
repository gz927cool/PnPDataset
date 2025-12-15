import os
import pandas as pd

enrich_dir = r"c:\Users\001\Desktop\list\04-Enrich"

# Define the updates
# Key: The current 'Main Entry' value
# Value: A dictionary of columns to update
updates = {
    "Strozzi": {"Main Entry": "Bernardo Strozzi", "Type": "E21 Person"},
    "Baccinelli": {"Main Entry": "Bernardine Baccinelli", "Type": "E21 Person"},
    
    # Obvious People
    "Charles I of England": {"Type": "E21 Person"},
    "Charles II of England": {"Type": "E21 Person"},
    "Catherine the Great of Russia": {"Type": "E21 Person"},
    "Baciccio": {"Type": "E21 Person"}, # Gaulli
    "Monsù Desiderio": {"Type": "E21 Person"}, # Artist
    "Bombelli Sebastiano": {"Type": "E21 Person"},
    "Caime": {"Type": "E21 Person"}, # Likely a person
    "Candiani": {"Type": "E21 Person"}, # Likely a person
    "Cebes": {"Type": "E21 Person"}, # Ancient Greek philosopher
    
    # Religious Orders / Groups
    "Benedictines": {"Type": "E74 Group"},
    "Capuchins": {"Type": "E74 Group"},
    "Carmelites": {"Type": "E74 Group"},
    "Barnabotti": {"Type": "E74 Group"},
    "Cavalieri di Santo Stefano": {"Type": "E74 Group"},
    
    # Concepts
    "Book illustration": {"Type": "E28 Conceptual Object"},
}

def update_csvs():
    files = [f for f in os.listdir(enrich_dir) if f.endswith(".csv")]
    total_updated = 0
    
    for filename in files:
        path = os.path.join(enrich_dir, filename)
        try:
            df = pd.read_csv(path)
            if 'Main Entry' not in df.columns:
                continue
                
            updated_in_file = 0
            
            # Iterate through the DataFrame and apply updates
            for index, row in df.iterrows():
                term = row['Main Entry']
                
                # Check if we have an update for this term
                if term in updates:
                    changes = updates[term]
                    for col, new_val in changes.items():
                        if col in df.columns:
                            df.at[index, col] = new_val
                            updated_in_file += 1
            
            if updated_in_file > 0:
                df.to_csv(path, index=False, encoding='utf-8-sig')
                print(f"Updated {updated_in_file} fields in {filename}")
                total_updated += updated_in_file
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    print(f"Total updates applied: {total_updated}")

if __name__ == "__main__":
    update_csvs()
