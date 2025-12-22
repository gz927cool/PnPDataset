import pandas as pd

path_06 = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\04-QID-Combine ORGfile\06-Requery_Filled_Cleaned.csv"
path_03 = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\03-LLM-Fillin-QID\03-LLM_Fillin_With_QID.csv"

def check():
    df06 = pd.read_csv(path_06)
    df03 = pd.read_csv(path_03)
    
    print("Searching for 'A.M. Zanetti' in 06...")
    match06 = df06[df06['Refined_Formal_Name'].str.contains("Zanetti", na=False)]
    print(match06)
    
    print("\nSearching for 'A.M. Zanetti' in 03...")
    match03 = df03[df03['原始名称 (CSV)'].str.contains("Zanetti", na=False)]
    print(match03[['原始名称 (CSV)', '英文正式名称 (Formal Name)', 'Matched_QID']])

if __name__ == "__main__":
    check()
