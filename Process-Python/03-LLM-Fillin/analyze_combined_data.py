import pandas as pd
import os

def analyze_dataset():
    file_path = r"c:\Users\001\Desktop\Github-Project\PnPDataset\09-MissingQID-LLM-Fillin\04-QID-Combine ORGfile\07-Requery_Filled_Combined.csv"
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    try:
        df = pd.read_csv(file_path)
        
        print("="*50)
        print("DATA ANALYSIS REPORT: 07-Requery_Filled_Combined.csv")
        print("="*50)
        
        # 1. Basic Stats
        total_rows = len(df)
        print(f"\n[1] Basic Information")
        print(f"Total Rows: {total_rows}")
        print(f"Columns: {df.columns.tolist()}")
        
        # 2. Missing Values & Coverage
        print(f"\n[2] QID Coverage Analysis")
        
        qid_cols = ['Original-QID', 'Second-Query_QID', 'LLM-Fillin_QID']
        
        # Ensure cols exist
        available_qid_cols = [c for c in qid_cols if c in df.columns]
        
        for col in available_qid_cols:
            non_null_count = df[col].notna().sum()
            # Also check for empty strings if they exist
            # non_empty_count = df[df[col].astype(str).str.strip() != ''].shape[0] 
            # (Assuming NaNs are properly handled by read_csv, but let's be safe)
            filled_rows = df[df[col].notna() & (df[col].astype(str).str.strip() != '')]
            count = len(filled_rows)
            percentage = (count / total_rows) * 100
            print(f"  - {col}: {count} rows filled ({percentage:.2f}%)")

        # 3. Overall Coverage (Any QID)
        # Create a boolean mask for rows that have at least one QID in any of the available columns
        def has_any_qid(row):
            for col in available_qid_cols:
                val = str(row[col]).strip()
                if pd.notna(row[col]) and val != '' and val.lower() != 'nan':
                    return True
            return False

        df['Has_Any_QID'] = df.apply(has_any_qid, axis=1)
        total_covered = df['Has_Any_QID'].sum()
        total_missing = total_rows - total_covered
        
        print(f"\n[3] Overall Completion")
        print(f"  - Rows with AT LEAST ONE QID: {total_covered} ({total_covered/total_rows*100:.2f}%)")
        print(f"  - Rows with NO QID: {total_missing} ({total_missing/total_rows*100:.2f}%)")
        
        # 4. Contribution of LLM-Fillin
        # How many rows ONLY have LLM-Fillin_QID and no others?
        if 'LLM-Fillin_QID' in df.columns:
            llm_only = df[
                (df['LLM-Fillin_QID'].notna()) & 
                (df['LLM-Fillin_QID'].astype(str).str.strip() != '') &
                (df['Original-QID'].isna() | (df['Original-QID'].astype(str).str.strip() == '')) &
                (df['Second-Query_QID'].isna() | (df['Second-Query_QID'].astype(str).str.strip() == ''))
            ]
            print(f"\n[4] LLM-Fillin Contribution")
            print(f"  - Rows uniquely filled by LLM-Fillin (filling gaps): {len(llm_only)}")
            
            # Check overlap: LLM-Fillin present AND others present
            llm_overlap = df[
                (df['LLM-Fillin_QID'].notna()) & 
                (df['LLM-Fillin_QID'].astype(str).str.strip() != '') &
                ((df['Original-QID'].notna()) | (df['Second-Query_QID'].notna()))
            ]
            print(f"  - Rows with LLM-Fillin overlapping with others: {len(llm_overlap)}")

        # 5. Split Data Detection
        print(f"\n[5] Split/Multiple QID Detection")
        for col in available_qid_cols:
            split_rows = df[df[col].astype(str).str.contains(';', na=False)]
            if not split_rows.empty:
                print(f"  - {col} has {len(split_rows)} rows with multiple QIDs (semicolon detected).")
                # print example
                # print(split_rows[col].head(1).values)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    analyze_dataset()
