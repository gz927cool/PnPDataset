import os
import pandas as pd

enrich_dir = r"c:\Users\001\Desktop\list\04-Enrich"

# Comprehensive mapping for remaining Unknowns
# Based on manual classification of the provided list
type_mapping = {
    # E21 Person
    'Baciccio': 'E21 Person',
    'Rosichino': 'E21 Person',
    'Charles XII of Sweden': 'E21 Person',
    'Cicero': 'E21 Person',
    'Cinelli': 'E21 Person',
    'Claude Lorrain': 'E21 Person',
    'Correggio': 'E21 Person',
    'Domenichino (Domenico Zampieri)': 'E21 Person',
    'Epicurus': 'E21 Person',
    'Fontenelle': 'E21 Person',
    'Frederick III (Holy Roman Emperor)': 'E21 Person',
    'Frederick IV of Denmark': 'E21 Person',
    'Frederick the Great': 'E21 Person',
    'Giotto': 'E21 Person',
    'Giulio Romano': 'E21 Person',
    'Gregory XIII': 'E21 Person',
    'Gregory XV': 'E21 Person',
    'Gustavus Adolphus of Sweden': 'E21 Person',
    'Gustavus III of Sweden': 'E21 Person',
    'Horace': 'E21 Person',
    'James II of England': 'E21 Person',
    'James III of England': 'E21 Person',
    'Johann Georg III of Saxony': 'E21 Person',
    'Julian the Apostate': 'E21 Person',
    'Justinus': 'E21 Person',
    'Justus of Ghent': 'E21 Person',
    'La Harpe': 'E21 Person',
    'Leonardo da Vinci': 'E21 Person',
    'Lorenzini': 'E21 Person',
    'Louis XIII': 'E21 Person',
    'Louis XIV': 'E21 Person',
    'Louis XV': 'E21 Person',
    'Machiavelli': 'E21 Person',
    'Mastelletta': 'E21 Person',
    'Montesquieu': 'E21 Person',
    'Padovanino': 'E21 Person',
    'Platnerus': 'E21 Person',
    'Pomerancio': 'E21 Person',
    'Rembrandt': 'E21 Person',
    'Remondini': 'E21 Person',
    'Riminaldi': 'E21 Person',
    'Sassoferrato (Giovan Battista Salvi)': 'E21 Person',
    'Seneca': 'E21 Person',
    'Shakespeare': 'E21 Person',
    'Sixtus V': 'E21 Person',
    'Stendhal': 'E21 Person',
    'Urban VIII': 'E21 Person',
    'Valentin de Boulogne': 'E21 Person',
    'Velasquez': 'E21 Person',
    'Virgil': 'E21 Person',
    'Vitruvius': 'E21 Person',
    'Voltaire': 'E21 Person',
    'William III of England': 'E21 Person',
    
    # E53 Place
    'Canons (Duke of Chandos)': 'E53 Place',
    'Dresden': 'E53 Place',
    'Dusseldorf': 'E53 Place',
    'Ferrara': 'E53 Place',
    'Genoa': 'E53 Place',
    'Louvre': 'E53 Place',
    'Lucca': 'E53 Place',
    'Macerata': 'E53 Place',
    'Madrid': 'E53 Place',
    'Manin country house': 'E53 Place',
    'Messina': 'E53 Place',
    'Padua': 'E53 Place',
    'Papal states': 'E53 Place',
    'Poggio a Caiano': 'E53 Place',
    'Pommersfelden': 'E53 Place',
    'Quirinal': 'E53 Place',
    'Savoy': 'E53 Place',
    'Turin': 'E53 Place',
    'Udine': 'E53 Place',
    'Vaduz': 'E53 Place',
    'Vicenza': 'E53 Place',
    'Vienna': 'E53 Place',
    'Widmann country house': 'E53 Place',
    
    # E74 Group
    'Congregazione dei Virtuosi': 'E74 Group',
    'Dutch artists': 'E74 Group',
    'Gesuati': 'E74 Group',
    'Gonzaga': 'E74 Group',
    'Oratorians': 'E74 Group',
    'Scalzi': 'E74 Group',
    'Theatines': 'E74 Group',
    'Cremonese': 'E74 Group', # Referring to people from Cremona or the school
    
    # E22 Man-Made Object
    'Baglioni collection': 'E22 Man-Made Object',
    'Bonfiglioli collection': 'E22 Man-Made Object',
    'Giovanelli collection': 'E22 Man-Made Object',
    'Grassi collection': 'E22 Man-Made Object',
    'Hapsburg collections from Prague': 'E22 Man-Made Object',
    'Imago primi saeculi': 'E22 Man-Made Object',
    'Labia collection': 'E22 Man-Made Object',
    'Royal Collection': 'E22 Man-Made Object',
    'Gazzeta Veneta': 'E22 Man-Made Object',
    'Osservatore Veneto': 'E22 Man-Made Object',
    'Illustrated books': 'E22 Man-Made Object',
    'Lot and his Daughters': 'E22 Man-Made Object', # Artwork title
    
    # E28 Conceptual Object
    'Competitions': 'E28 Conceptual Object',
    'Contracts': 'E28 Conceptual Object',
    'Customs duty on pictures': 'E28 Conceptual Object',
    'English patronage': 'E28 Conceptual Object',
    'English tourists in Italy': 'E28 Conceptual Object',
    'Enlightenment in Italy': 'E28 Conceptual Object',
    'Fantasy and reason': 'E28 Conceptual Object',
    'French hostility to Italian art in the 17th century': 'E28 Conceptual Object',
    'French patronage': 'E28 Conceptual Object',
    'German patronage': 'E28 Conceptual Object',
    'Hapsburg patronage of Venetian artists': 'E28 Conceptual Object',
    'Indecency and the erotic': 'E28 Conceptual Object',
    'Indecency in art': 'E28 Conceptual Object',
    'Mannerist painting': 'E28 Conceptual Object',
    'Modelli': 'E28 Conceptual Object',
    'Nationalism and art': 'E28 Conceptual Object',
    'Oratorio': 'E28 Conceptual Object',
    'Patron-artist relation': 'E28 Conceptual Object',
    'Prices paid to artists': 'E28 Conceptual Object',
    'Provincial centres of art patronage': 'E28 Conceptual Object',
    'Reason and fantasy': 'E28 Conceptual Object',
    'Servizio particolare': 'E28 Conceptual Object',
    'Social position of the artist': 'E28 Conceptual Object',
    'Spanish patronage': 'E28 Conceptual Object',
    'Stoicism in 17th century': 'E28 Conceptual Object',
    'Titles granted to artists': 'E28 Conceptual Object',
}

def apply_updates():
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
                
                # Handle encoding issues for specific terms
                if "Mons" in term and "Desiderio" in term:
                    term = "Monsù Desiderio" # Normalize key
                if "W" in term and "rzburg" in term:
                    term = "Würzburg Residenz" # Normalize key
                
                # Check if we have a mapping
                if term in type_mapping:
                    new_type = type_mapping[term]
                    if current_type != new_type:
                        df.at[index, 'Type'] = new_type
                        updated_in_file += 1
                
                # Also handle the encoding-mangled keys directly if they exist in the dict
                # (The dict above uses clean keys, but the CSV might have mangled ones)
                # We'll rely on the exact string match from the CSV unless we fuzzy match
                
                # Fuzzy match for the mangled ones
                if "Mons" in str(row['Main Entry']) and "Desiderio" in str(row['Main Entry']):
                     if current_type != 'E21 Person':
                        df.at[index, 'Type'] = 'E21 Person'
                        updated_in_file += 1
                
                if "W" in str(row['Main Entry']) and "rzburg" in str(row['Main Entry']):
                     if current_type != 'E53 Place':
                        df.at[index, 'Type'] = 'E53 Place'
                        updated_in_file += 1

            if updated_in_file > 0:
                df.to_csv(path, index=False, encoding='utf-8-sig')
                print(f"Updated {updated_in_file} entries in {filename}")
                total_updated += updated_in_file
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    print(f"Total updates applied: {total_updated}")

if __name__ == "__main__":
    apply_updates()
