import pandas as pd
import os

csv_path = r"d:\my_project\PnPDataset\18-Triplet-Link\data\kb_solokb_solo\data\output\alignment_result.csv"

if os.path.exists(csv_path):
    print(f"Reading {csv_path}...")
    # Read with pandas (which handles multiline quotes correctly)
    df = pd.read_csv(csv_path)
    
    # Replace newlines in 'notes' column
    if 'notes' in df.columns:
        print("Cleaning 'notes' column...")
        df['notes'] = df['notes'].astype(str).apply(lambda x: x.replace('\n', ' ').replace('\r', ' '))
    
    # Save back
    print(f"Saving to {csv_path}...")
    df.to_csv(csv_path, index=False)
    print("Done.")
else:
    print(f"File not found: {csv_path}")
