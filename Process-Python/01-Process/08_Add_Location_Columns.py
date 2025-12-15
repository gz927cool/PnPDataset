import os
import pandas as pd

enrich_dir = r"c:\Users\001\Desktop\list\04-Enrich"

# Comprehensive Knowledge Base for Location Enrichment
# Based on standard Art History (Patrons and Painters context)
location_map = {
    # A
    "Accademia di S. Luca": "Rome",
    "Accademia del Disegno": "Florence",
    "Accademia dei Lincei": "Rome",
    "Accademia degli Umoristi": "Rome",
    "Accademia Albrizziana": "Venice",
    "Accademia di Pittura e Scultura": "Rome", # Often refers to St Luke or French Academy in Rome
    "Adam, Robert": "London/Rome",
    "Adam, James": "London/Rome",
    "Agucchi, Giovanni Battista": "Rome",
    "Albani, Cardinal Annibale": "Rome",
    "Albani, Francesco": "Bologna",
    "Albani, Gianfrancesco (Pope Clement XI)": "Rome",
    "Aldobrandini, Cardinal Pietro": "Rome",
    "Aldobrandini, Ippolito (Pope Clement VIII)": "Rome",
    "Alexander VII": "Rome",
    "Alexander VIII": "Rome",
    "Algardi, Alessandro": "Rome",
    "Algarotti, Francesco": "Venice/Berlin",
    "Amigoni, Jacopo": "Venice",
    "Anne of Austria": "Paris",
    "Anne, Queen of England": "London",
    "Arpino, Cavaliere d'": "Rome",
    "Arundel, Lord": "London",
    
    # B
    "'Baciccio'": "Rome",
    "Bernardine Baccinelli": "Rome",
    "Bacon, Sir Francis": "London",
    "Baglione, Giovanni": "Rome",
    "Bagutti, Pietro Martire": "Bologna",
    "Baldinucci, Filippo": "Florence",
    "Balestra, Antonio": "Verona/Venice",
    "Bamboccianti": "Rome",
    "Barberini family": "Rome",
    "Barberini, Maffeo (Pope Urban VIII)": "Rome",
    "Barberini, Cardinal Francesco": "Rome",
    "Barberini, Cardinal Antonio": "Rome",
    "Barbieri, Giovanni Francesco (Guercino)": "Bologna/Rome",
    "Barocci, Federico": "Urbino",
    "Bartoli, Pietro Santi": "Rome",
    "Baschenis, Evaristo": "Bergamo",
    "Bassano, Jacopo": "Venice",
    "Batoni, Pompeo": "Rome",
    "Bellori, Giovan Pietro": "Rome",
    "Bernini, Gian Lorenzo": "Rome",
    "Bibiena family": "Bologna",
    "Bombelli, Sebastiano": "Venice",
    "Borromini, Francesco": "Rome",
    "Boucher, François": "Paris",
    "Brandi, Giacinto": "Rome",
    "Burlington, Lord": "London",
    
    # C
    "Cagnacci, Guido": "Bologna/Venice",
    "Canaletto": "Venice/London",
    "Canova, Antonio": "Rome/Venice",
    "Caracci, Agostino": "Bologna/Rome",
    "Caracci, Annibale": "Bologna/Rome",
    "Caracci, Lodovico": "Bologna",
    "Caravaggio": "Rome",
    "Carlone, Carlo": "Como/Austria",
    "Carriera, Rosalba": "Venice",
    "Castiglione, Giovanni Benedetto": "Genoa/Rome",
    "Catherine the Great of Russia": "St. Petersburg",
    "Cavallino, Bernardo": "Naples",
    "Cavedone, Giacomo": "Bologna",
    "Charles I of England": "London",
    "Charles II of England": "London",
    "Chigi, Agostino": "Rome",
    "Chigi, Fabio (Pope Alexander VII)": "Rome",
    "Christina, Queen of Sweden": "Rome", # Settled in Rome
    "Cignani, Carlo": "Bologna",
    "Cigoli, Lodovico": "Florence/Rome",
    "Claude Lorrain": "Rome",
    "Clement VIII": "Rome",
    "Clement IX": "Rome",
    "Clement X": "Rome",
    "Clement XI": "Rome",
    "Clement XII": "Rome",
    "Colonna family": "Rome",
    "Colonna, Prince Lorenzo Onofrio": "Rome",
    "Conca, Sebastiano": "Rome/Naples",
    "Cortona, Pietro da": "Rome/Florence",
    "Crespi, Giuseppe Maria": "Bologna",
    
    # D
    "Diziani, Gaspare": "Venice",
    "Dolci, Carlo": "Florence",
    "Domenichino (Domenico Zampieri)": "Rome/Bologna",
    "Doria family": "Genoa/Rome",
    "Dughet, Gaspard": "Rome",
    "Duquesnoy, François": "Rome",
    
    # E
    "Edwards, Pietro": "Venice",
    "Elsheimer, Adam": "Rome",
    
    # F
    "Falcone, Aniello": "Naples",
    "Farnese family": "Parma/Rome",
    "Farnese, Cardinal Odoardo": "Rome",
    "Fetti, Domenico": "Mantua/Venice",
    "Fiammingo (Duquesnoy)": "Rome",
    "Fontana, Carlo": "Rome",
    "Franceschini, Marcantonio": "Bologna",
    "Frederick the Great": "Berlin/Potsdam",
    "Fuga, Ferdinando": "Rome/Naples",
    "Furini, Francesco": "Florence",
    
    # G
    "Galli-Bibiena": "Bologna",
    "Gaulli, Giovanni Battista (Baciccio)": "Rome",
    "Gentileschi, Artemisia": "Rome/Naples",
    "Gentileschi, Orazio": "Rome/London",
    "Ghezzi, Pier Leone": "Rome",
    "Giaquinto, Corrado": "Rome/Madrid",
    "Giordano, Luca": "Naples/Florence/Madrid",
    "Giorgione": "Venice",
    "Giustiniani, Marchese Vincenzo": "Rome",
    "Gonzaga family": "Mantua",
    "Grassi, Nicola": "Venice",
    "Gregory XV": "Rome",
    "Guardi, Francesco": "Venice",
    "Guardi, Gian Antonio": "Venice",
    "Guercino": "Bologna/Rome",
    "Guidi, Domenico": "Rome",
    
    # H
    "Hamilton, Gavin": "Rome",
    "Hapsburg family": "Vienna/Madrid",
    
    # I
    "Innocent X": "Rome",
    "Innocent XI": "Rome",
    "Innocent XII": "Rome",
    
    # J
    "Juvarra, Filippo": "Turin",
    
    # L
    "Lanfranco, Giovanni": "Rome/Naples",
    "Largillierre, Nicolas de": "Paris",
    "Lazzarini, Gregorio": "Venice",
    "Le Brun, Charles": "Paris",
    "Leo XI": "Rome",
    "Leopold I, Emperor": "Vienna",
    "Liberi, Pietro": "Venice",
    "Longhi, Pietro": "Venice",
    "Loth, Johann Carl": "Venice",
    "Louis XIII": "Paris",
    "Louis XIV": "Paris",
    "Louis XV": "Paris",
    "Ludovisi, Cardinal Ludovico": "Rome",
    "Luti, Benedetto": "Rome",
    
    # M
    "Maderno, Carlo": "Rome",
    "Maffei, Scipione": "Verona",
    "Magnasco, Alessandro": "Genoa/Milan",
    "Manfredi, Bartolomeo": "Rome",
    "Maratta, Carlo": "Rome",
    "Marini, Giambattista": "Rome/Paris",
    "Massimi, Cardinal Camillo": "Rome",
    "Mazarin, Cardinal": "Paris",
    "Mazza, Damiano": "Venice",
    "Medici family": "Florence",
    "Medici, Cardinal Leopoldo de'": "Florence",
    "Medici, Cosimo III de'": "Florence",
    "Medici, Marie de'": "Paris",
    "Mengs, Anton Raphael": "Rome/Madrid",
    "Mola, Pier Francesco": "Rome",
    "Molinarolo (Baccinelli)": "Rome", # Assuming context
    "Monsù Desiderio": "Naples",
    "Muratori, Ludovico Antonio": "Modena",
    
    # N
    "Napoletano, Filippo": "Rome/Naples",
    "Neri, San Filippo": "Rome",
    "Newton, Sir Isaac": "London",
    
    # O
    "Odescalchi family": "Rome",
    "Odescalchi, Benedetto (Pope Innocent XI)": "Rome",
    "Oratorians": "Rome",
    "Orsini family": "Rome",
    "Ottoboni, Cardinal Pietro": "Rome",
    
    # P
    "Pamfili family": "Rome",
    "Pamfili, Camillo": "Rome",
    "Pamfili, Giovanni Battista (Pope Innocent X)": "Rome",
    "Panini, Giovanni Paolo": "Rome",
    "Parodi, Filippo": "Genoa",
    "Pasinelli, Lorenzo": "Bologna",
    "Passeri, Giovanni Battista": "Rome",
    "Paul V": "Rome",
    "Pellegrini, Giovanni Antonio": "Venice",
    "Peretti, Felice (Pope Sixtus V)": "Rome",
    "Piazzetta, Giovanni Battista": "Venice",
    "Pietro da Cortona": "Rome",
    "Piles, Roger de": "Paris",
    "Piranesi, Giovanni Battista": "Rome",
    "Pittoni, Giambattista": "Venice",
    "Poussin, Nicolas": "Rome",
    "Pozzo, Andrea": "Rome/Vienna",
    "Preti, Mattia": "Naples/Malta",
    "Procaccini, Giulio Cesare": "Milan",
    
    # R
    "Raggi, Antonio": "Rome",
    "Raphael": "Rome",
    "Reni, Guido": "Bologna/Rome",
    "Reynolds, Sir Joshua": "London",
    "Ribera, Jusepe de": "Naples",
    "Riccardi family": "Florence",
    "Ricci, Marco": "Venice",
    "Ricci, Sebastiano": "Venice",
    "Richelieu, Cardinal": "Paris",
    "Rigaud, Hyacinthe": "Paris",
    "Rosa, Salvator": "Rome/Florence",
    "Rospigliosi family": "Rome",
    "Rospigliosi, Giulio (Pope Clement IX)": "Rome",
    "Rubens, Peter Paul": "Antwerp",
    "Rusconi, Camillo": "Rome",
    "Ruspoli, Prince Francesco Maria": "Rome",
    
    # S
    "Sacchi, Andrea": "Rome",
    "Sacchetti family": "Rome",
    "Sacchetti, Cardinal Giulio": "Rome",
    "Sandrart, Joachim von": "Rome/Nuremberg",
    "Sassoferrato (Giovan Battista Salvi)": "Rome",
    "Scarlatti, Alessandro": "Rome/Naples",
    "Sebastiano del Piombo": "Rome",
    "Serodine, Giovanni": "Rome",
    "Shaftesbury, Lord": "London",
    "Sixtus V": "Rome",
    "Smith, Joseph (Consul Smith)": "Venice",
    "Solimena, Francesco": "Naples",
    "Spada, Cardinal Bernardino": "Rome",
    "Spinola family": "Genoa",
    "Strozzi, Bernardo": "Genoa/Venice",
    "Subleyras, Pierre": "Rome",
    
    # T
    "Tassi, Agostino": "Rome",
    "Tempesta, Antonio": "Rome",
    "Teniers, David the Younger": "Antwerp",
    "Testa, Pietro": "Rome",
    "Theatines": "Rome",
    "Tiepolo, Giambattista": "Venice/Würzburg/Madrid",
    "Tiepolo, Giandomenico": "Venice",
    "Tintoretto": "Venice",
    "Titian": "Venice",
    "Trevisani, Francesco": "Rome",
    
    # U
    "Urban VIII": "Rome",
    
    # V
    "Vaccaro, Andrea": "Naples",
    "Valentin de Boulogne": "Rome",
    "Van Dyck, Anthony": "London/Antwerp/Genoa",
    "Vanvitelli, Gaspare": "Rome",
    "Vanvitelli, Luigi": "Naples",
    "Vasari, Giorgio": "Florence",
    "Velasquez": "Madrid",
    "Venice": "Venice",
    "Veronese, Paolo": "Venice",
    "Vleughels, Nicolas": "Rome",
    "Volterrano (Baldassarre Franceschini)": "Florence",
    "Vouet, Simon": "Rome/Paris",
    
    # W
    "Walpole, Horace": "London",
    "Watteau, Antoine": "Paris",
    "Winckelmann, Johann Joachim": "Rome",
    "Wootton, John": "London",
    "Wren, Sir Christopher": "London",
    
    # Z
    "Zanetti, Anton Maria": "Venice",
    "Zuccarelli, Francesco": "Venice/London",
    "Zuccaro, Federico": "Rome"
}

def enrich_files():
    print("--- Applying Location Enrichment ---")
    files = [f for f in os.listdir(enrich_dir) if f.endswith("_refined.csv")]
    
    total_updated = 0
    
    for filename in files:
        path = os.path.join(enrich_dir, filename)
        try:
            df = pd.read_csv(path)
            
            # Add new columns if they don't exist
            if 'Proposed Location' not in df.columns:
                df['Proposed Location'] = ""
            if 'Notes' not in df.columns:
                df['Notes'] = ""
            
            updated_in_file = 0
            
            for index, row in df.iterrows():
                term = str(row['Index_Main Entry']).strip()
                clean_term = term.strip("'")
                
                # Determine location
                loc = ""
                note = ""
                
                if term in location_map:
                    loc = location_map[term]
                    note = "Auto-enriched from Knowledge Base"
                elif clean_term in location_map:
                    loc = location_map[clean_term]
                    note = "Auto-enriched from Knowledge Base"
                
                # If we found a location, update the row
                if loc:
                    # Only update if empty or we want to overwrite (here we fill empty)
                    if pd.isna(row['Proposed Location']) or row['Proposed Location'] == "":
                        df.at[index, 'Proposed Location'] = loc
                        df.at[index, 'Notes'] = note
                        updated_in_file += 1
            
            if updated_in_file > 0 or 'Proposed Location' not in df.columns: # Save if we added columns or data
                df.to_csv(path, index=False, encoding='utf-8-sig')
                print(f"Enriched {filename}: {updated_in_file} entries updated")
                total_updated += 1
            else:
                # Ensure columns exist even if no data matches
                df.to_csv(path, index=False, encoding='utf-8-sig')
                print(f"Processed {filename}: Columns added, 0 matches found")
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    print(f"Total files processed: {total_updated}")

if __name__ == "__main__":
    enrich_files()
