import pandas as pd
import os
import glob

def generate_consolidated_report():
    base_dir = r'c:\Users\001\Desktop\Github-Project\PnPDataset'
    input_dir = os.path.join(base_dir, "06-Crosscheck")
    output_file = os.path.join(input_dir, "All_Entries_Comparison.csv")
    
    csv_files = glob.glob(os.path.join(input_dir, "*_crosscheck.csv"))
    
    all_data = []
    
    print(f"Consolidating {len(csv_files)} files...")
    
    for filepath in csv_files:
        filename = os.path.basename(filepath)
        # Extract letter code (e.g., "A" from "A_crosscheck.csv")
        file_code = filename.replace("_crosscheck.csv", "")
        
        try:
            df = pd.read_csv(filepath)
            
            # Select specific columns for the report
            report_df = pd.DataFrame()
            report_df['File_Code'] = [file_code] * len(df)
            report_df['Index_Entry'] = df['Index_Main Entry']
            report_df['CIDOC_Type'] = df['CIDOC_Type']
            
            # Handle potential missing columns if script failed partially (unlikely but safe)
            report_df['Matched_QID'] = df.get('Matched_QID', '')
            report_df['Matched_Name'] = df.get('Matched_Name', '')
            report_df['Match_Type'] = df.get('Match_Type', '')
            report_df['Match_Source'] = df.get('Match_Source', '')
            
            # Determine Status
            report_df['Status'] = report_df['Matched_QID'].apply(
                lambda x: 'Matched' if pd.notna(x) and str(x).strip() != '' else 'Unmatched'
            )
            
            all_data.append(report_df)
            
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        
        # Sort by Status (Unmatched first for visibility?) or File Code. 
        # Let's sort by File Code then Index Entry
        final_df.sort_values(by=['File_Code', 'Index_Entry'], inplace=True)
        
        final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"Successfully generated consolidated report: {output_file}")
        print(f"Total Entries: {len(final_df)}")
        print(f"Matched: {len(final_df[final_df['Status'] == 'Matched'])}")
        print(f"Unmatched: {len(final_df[final_df['Status'] == 'Unmatched'])}")
    else:
        print("No data found to consolidate.")

if __name__ == "__main__":
    generate_consolidated_report()
