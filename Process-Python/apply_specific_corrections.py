import pandas as pd
import os

# Define paths
base_dir = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\07-Human-Merge"
input_file = os.path.join(base_dir, "04-Requery_Filled_Human_Merged_Final.csv")
output_file = os.path.join(base_dir, "06-Requery_Filled_Human_Merged_Corrected.csv")

# Read the CSV
df = pd.read_csv(input_file)

# Define corrections
# Key: Refined_Formal_Name, Value: New QID
corrections = {
    "Zeuxis": "Q197044",
    "Zechariah": "Q139464",
    "Theresa of Avila (人物)": "Q174880",
    "Teresa of Ávila": "Q174880",
    "Theseus": "Q1320718"
}

print("Applying corrections...")

updated_count = 0

for name, new_qid in corrections.items():
    # Find rows matching the name
    mask = df['Refined_Formal_Name'] == name
    
    if mask.any():
        # Update QID
        df.loc[mask, 'Original-QID'] = new_qid
        count = mask.sum()
        updated_count += count
        print(f"Updated {count} row(s) for '{name}' to QID {new_qid}")
    else:
        print(f"Name '{name}' not found in dataset.")

# Save
df.to_csv(output_file, index=False)
print("-" * 30)
print(f"Total rows updated: {updated_count}")
print(f"Saved corrected file to {output_file}")
