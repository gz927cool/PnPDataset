import pandas as pd
from src.config import config
import os

def clean_relations_mapping():
    print("Cleaning up duplicates in relations_mapping.csv...")
    if not os.path.exists(config.RELATIONS_MAPPING_PATH):
        print("File not found, nothing to clean.")
        return

    try:
        df = pd.read_csv(config.RELATIONS_MAPPING_PATH)
        initial_count = len(df)
        
        # De-duplicate: strictly unique rows
        df_clean = df.drop_duplicates()
        
        final_count = len(df_clean)
        
        df_clean.to_csv(config.RELATIONS_MAPPING_PATH, index=False)
        print(f"Cleaned relations_mapping.csv: {initial_count} -> {final_count} rows. Removed {initial_count - final_count} duplicates.")
        
    except Exception as e:
        print(f"Error cleaning file: {e}")

if __name__ == "__main__":
    clean_relations_mapping()
