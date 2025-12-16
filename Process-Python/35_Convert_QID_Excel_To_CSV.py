import pandas as pd
import os

# Define paths
base_dir = r"c:\Users\001\Desktop\Github-Project\PnPDataset"
input_file = os.path.join(base_dir, "08-Data-Remerge", "04-Merged_Recheck_With_QID.xlsx")
output_file = os.path.join(base_dir, "08-Data-Remerge", "04-Merged_Recheck_With_QID.csv")

def convert_excel_to_csv():
    print(f"Loading Excel file from {input_file}...")
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return

    try:
        df = pd.read_excel(input_file)
        print(f"Successfully loaded {len(df)} rows.")
        
        print(f"Saving to CSV file at {output_file}...")
        # Use utf-8-sig for better compatibility with Excel when opening CSVs containing Chinese characters
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print("Conversion complete.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    convert_excel_to_csv()
