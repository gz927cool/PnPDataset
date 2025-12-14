import pandas as pd
import os
import glob

def main():
    base_dir = r'c:\Users\001\Desktop\Github-Project\PnPDataset'
    handmade_dir = os.path.join(base_dir, "05-HandmadeDataset")
    crosscheck_dir = os.path.join(base_dir, "06-Crosscheck")
    output_file = os.path.join(crosscheck_dir, "Full_Comparison_Matrix.csv")

    # 1. Load Manual Data (05)
    print("Loading Manual Data...")
    manual_entries = {} # Key -> {Info, Used}
    
    manual_files = ["name-English_table.csv", "gio-English_table.csv", "work-English_table.csv"]
    
    for fname in manual_files:
        fpath = os.path.join(handmade_dir, fname)
        if os.path.exists(fpath):
            try:
                df = pd.read_csv(fpath, encoding='gbk')
                # Columns: QID, 统一英文全名
                name_col = '统一英文全名'
                if name_col not in df.columns:
                    print(f"Skipping {fname}, column {name_col} not found.")
                    continue
                
                for _, row in df.iterrows():
                    qid = str(row.get('QID', '')).strip()
                    name = str(row.get(name_col, '')).strip()
                    
                    # Normalize nan
                    if qid.lower() == 'nan': qid = ""
                    if name.lower() == 'nan': name = ""
                    
                    # Use QID as primary key if available, else Name
                    key = qid if qid else name
                    
                    if key:
                        manual_entries[key] = {
                            'Manual_Name': name,
                            'Manual_QID': qid,
                            'Manual_Source': fname,
                            'Used': False
                        }
            except Exception as e:
                print(f"Error reading {fname}: {e}")

    print(f"Loaded {len(manual_entries)} manual entries.")

    # 2. Process Crosscheck Data (06)
    print("Processing Crosscheck Data...")
    report_rows = []
    
    csv_files = glob.glob(os.path.join(crosscheck_dir, "*_crosscheck.csv"))
    
    for fpath in csv_files:
        fname = os.path.basename(fpath)
        file_code = fname.replace("_crosscheck.csv", "")
        
        try:
            df = pd.read_csv(fpath)
            
            for _, row in df.iterrows():
                # Extract Index Info
                idx_entry = row.get('Index_Main Entry', '')
                idx_type = row.get('CIDOC_Type', '')
                
                if pd.isna(idx_entry): continue
                
                # Extract Match Info
                matched_qid = str(row.get('Matched_QID', '')).strip()
                matched_name = str(row.get('Matched_Name', '')).strip()
                match_type = str(row.get('Match_Type', '')).strip()
                
                if matched_qid.lower() == 'nan': matched_qid = ""
                if matched_name.lower() == 'nan': matched_name = ""
                if match_type.lower() == 'nan': match_type = ""
                
                status = "Unmatched (Index)"
                
                # Check if matched
                is_matched = False
                
                # Try to mark as used in manual_entries
                if matched_qid and matched_qid in manual_entries:
                    manual_entries[matched_qid]['Used'] = True
                    is_matched = True
                elif matched_name and matched_name in manual_entries:
                    manual_entries[matched_name]['Used'] = True
                    is_matched = True
                
                # Even if not in manual_entries (maybe mismatch in loading?), if CSV says matched, we trust it
                if matched_qid or matched_name:
                    status = "Matched"
                    is_matched = True

                report_rows.append({
                    'Source_Side': 'Index',
                    'File_Code': file_code,
                    'Index_Entry': idx_entry,
                    'CIDOC_Type': idx_type,
                    'Manual_Name': matched_name,
                    'Manual_QID': matched_qid,
                    'Match_Type': match_type,
                    'Status': status
                })
                
        except Exception as e:
            print(f"Error processing {fname}: {e}")

    # 3. Add Unused Manual Entries
    print("Adding Unused Manual Entries...")
    unused_count = 0
    for key, info in manual_entries.items():
        if not info['Used']:
            report_rows.append({
                'Source_Side': 'Manual',
                'File_Code': info['Manual_Source'],
                'Index_Entry': "",
                'CIDOC_Type': "",
                'Manual_Name': info['Manual_Name'],
                'Manual_QID': info['Manual_QID'],
                'Match_Type': "",
                'Status': "Unmatched (Manual)"
            })
            unused_count += 1
            
    print(f"Added {unused_count} unused manual entries.")

    # 4. Save
    final_df = pd.DataFrame(report_rows)
    cols = ['Source_Side', 'Status', 'File_Code', 'Index_Entry', 'CIDOC_Type', 'Manual_Name', 'Manual_QID', 'Match_Type']
    final_df = final_df[cols]
    
    # Sort: Matched first, then Unmatched Index, then Unmatched Manual
    # Helper for sorting
    status_order = {'Matched': 0, 'Unmatched (Index)': 1, 'Unmatched (Manual)': 2}
    final_df['Sort_Key'] = final_df['Status'].map(status_order)
    final_df.sort_values(by=['Sort_Key', 'File_Code', 'Index_Entry'], inplace=True)
    final_df.drop(columns=['Sort_Key'], inplace=True)
    
    final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Report saved to {output_file}")
    print(f"Total Rows: {len(final_df)}")

if __name__ == "__main__":
    main()
