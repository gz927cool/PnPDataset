import os
import pandas as pd
from collections import Counter

enrich_dir = r"c:\Users\001\Desktop\list\04-Enrich"

def list_missing_terms():
    print("--- Top Missing Terms Analysis ---")
    files = [f for f in os.listdir(enrich_dir) if f.endswith("_refined.csv")]
    
    missing_terms = []
    
    for filename in files:
        path = os.path.join(enrich_dir, filename)
        try:
            df = pd.read_csv(path)
            # Filter for rows where Proposed Location is empty or NaN
            missing_df = df[df['Proposed Location'].isna() | (df['Proposed Location'] == "")]
            
            terms = missing_df['Index_Main Entry'].astype(str).tolist()
            missing_terms.extend(terms)
            
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    # Count frequencies
    counter = Counter(missing_terms)
    
    print(f"Total unique missing terms: {len(counter)}")
    print("\nTop 50 most frequent missing terms:")
    print("-" * 40)
    for term, count in counter.most_common(50):
        print(f"{term}: {count}")

    # Also write to a file to avoid console encoding issues if any
    with open(r"c:\Users\001\Desktop\list\99-Python\missing_terms_report.txt", "w", encoding="utf-8") as f:
        for term, count in counter.most_common():
            f.write(f"{term}\n")

if __name__ == "__main__":
    list_missing_terms()
