import pandas as pd
import os

def deduplicate_matrix():
    base_dir = r'c:\Users\001\Desktop\Github-Project\PnPDataset'
    input_file = os.path.join(base_dir, r'06-Crosscheck\Full_Comparison_Matrix.csv')
    output_file = os.path.join(base_dir, r'06-Crosscheck\Full_Comparison_Matrix_Unique.csv')
    
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return

    print(f"Loading {input_file}...")
    df = pd.read_csv(input_file)
    original_count = len(df)
    
    print(f"Original rows: {original_count}")
    
    # Fill NaNs to ensure grouping works correctly
    df.fillna('', inplace=True)
    
    # Define columns to group by (everything except File_Code)
    # We want to consolidate the same entry appearing in multiple files or multiple times
    group_cols = [
        'Source_Side', 
        'Status', 
        'Index_Entry', 
        'CIDOC_Type', 
        'Manual_Name', 
        'Manual_QID', 
        'Match_Type'
    ]
    
    # Aggregation logic: Join unique File_Codes
    print("Deduplicating and aggregating File_Codes...")
    df_unique = df.groupby(group_cols)['File_Code'].apply(
        lambda x: ', '.join(sorted(set([str(i) for i in x if i])))
    ).reset_index()
    
    # Sort again for readability
    # Helper for sorting Status
    status_order = {'Matched': 0, 'Unmatched (Index)': 1, 'Unmatched (Manual)': 2}
    df_unique['Sort_Key'] = df_unique['Status'].map(status_order)
    
    df_unique.sort_values(by=['Sort_Key', 'Index_Entry', 'Manual_Name'], inplace=True)
    df_unique.drop(columns=['Sort_Key'], inplace=True)
    
    # Reorder columns to put File_Code at the end or appropriate place
    cols = ['Source_Side', 'Status', 'Index_Entry', 'CIDOC_Type', 'Manual_Name', 'Manual_QID', 'Match_Type', 'File_Code']
    df_unique = df_unique[cols]
    
    final_count = len(df_unique)
    print(f"Unique rows: {final_count}")
    print(f"Removed {original_count - final_count} duplicate rows.")
    
    df_unique.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Saved unique matrix to: {output_file}")

if __name__ == "__main__":
    deduplicate_matrix()
