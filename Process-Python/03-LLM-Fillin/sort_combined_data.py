import pandas as pd
import os

def sort_dataset():
    file_path = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\04-QID-Combine ORGfile\07-Requery_Filled_Combined.csv"
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    try:
        df = pd.read_csv(file_path)
        print(f"Original shape: {df.shape}")
        
        if 'Refined_Formal_Name' not in df.columns:
            print("Error: Column 'Refined_Formal_Name' not found in dataset.")
            print("Available columns:", df.columns.tolist())
            return
            
        # Sort by Refined_Formal_Name
        # Use a key to handle non-string values gracefully if any, though they should be strings.
        # fillna('') ensures NaN values are treated as empty strings and don't cause errors, 
        # usually placing them at the beginning.
        df_sorted = df.sort_values(by='Refined_Formal_Name', key=lambda x: x.fillna('').astype(str).str.lower())
        
        # Save back to the same file
        df_sorted.to_csv(file_path, index=False)
        print(f"Successfully sorted dataset by 'Refined_Formal_Name'. Saved to {file_path}")
        print(f"New shape: {df_sorted.shape}")
        
        # Display first few rows to verify
        print("\nFirst 5 rows after sorting:")
        print(df_sorted[['Refined_Formal_Name']].head())

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    sort_dataset()
