import pandas as pd
import os

path = r"c:\Users\001\Desktop\list\04-Enrich\B_refined.csv"
df = pd.read_csv(path)

# Simulated Knowledge Base (In a real full run, this would be populated by the Agent/API)
# Mapping: Main Entry -> Location
knowledge_base = {
    "'Baciccio'": "Rome", # Gaulli
    "Bernardine Baccinelli": "Rome", # Likely Gaulli/Baciccio variant
    "Bacon, Sir Francis": "London",
    "Baglione, Giovanni": "Rome",
    "Bagutti, Pietro Martire": "Bologna",
    "Baines, Sir Thomas": "Cambridge/Constantinople", # English physician
    "Baker, Thomas": "London",
    "Baldinucci, Filippo": "Florence",
    "Balestra, Antonio": "Verona",
    "Bandini, Cardinal": "Rome",
    "Bandini, Ottavio": "Rome",
    "Barberini, Cardinal Antonio": "Rome",
    "Barberini, Cardinal Francesco": "Rome",
    "Barberini, Maffeo (Pope Urban VIII)": "Rome",
    "Barberini family": "Rome",
    "Barbieri, Giovanni Francesco (Guercino)": "Bologna/Rome",
    "Barocci, Federico": "Urbino",
    "Bartoli, Pietro Santi": "Rome",
    "Baschenis, Evaristo": "Bergamo",
    "Bassano, Jacopo": "Venice",
    "Batoni, Pompeo": "Rome",
    "Bellori, Giovan Pietro": "Rome",
    "Bernini, Gian Lorenzo": "Rome",
    "Bibiena family": "Bologna",
    "Bologna": "Bologna", # It's a place
    "Borromini, Francesco": "Rome"
}

print("--- Proposed Location Enrichment for B_refined.csv (Preview) ---")
print(f"{'Main Entry':<50} | {'Current Location':<20} | {'Proposed Location':<20}")
print("-" * 95)

count = 0
for index, row in df.iterrows():
    term = row['Index_Main Entry']
    current_loc = str(row['Index_Location'])
    if current_loc == 'nan': current_loc = ""
    
    # Check if we have a match in our KB
    # Handle quotes in term
    clean_term = term.strip("'")
    
    proposed = ""
    if term in knowledge_base:
        proposed = knowledge_base[term]
    elif clean_term in knowledge_base:
        proposed = knowledge_base[clean_term]
    
    # Only show if we have a proposal and it's different/new
    if proposed and proposed != current_loc:
        print(f"{term:<50} | {current_loc:<20} | {proposed:<20}")
        count += 1
        if count >= 20: # Limit preview
            break

print("-" * 95)
print(f"Total proposed updates in this preview: {count}")
