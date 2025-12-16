import pandas as pd
import os

# Define paths
base_dir = r"c:\Users\001\Desktop\Github-Project\PnPDataset"
input_file = os.path.join(base_dir, "08-Data-Remerge", "02-Merged_Recheck_Deduplicated.csv")
output_report = os.path.join(base_dir, "08-Data-Remerge", "Deduplication_Audit_Report.txt")

def analyze_deduplicated_data():
    print(f"Loading data from {input_file}...")
    try:
        df = pd.read_csv(input_file, encoding='utf-8-sig')
    except:
        df = pd.read_csv(input_file, encoding='gbk')

    report_lines = []
    report_lines.append("=== Deduplication Audit Report ===\n")
    report_lines.append(f"Total Rows: {len(df)}")
    
    # 1. Sanity Check for Duplicates
    duplicates = df.duplicated(subset=['Refined_Formal_Name'], keep=False)
    num_duplicates = duplicates.sum()
    report_lines.append(f"Remaining Duplicates in 'Refined_Formal_Name': {num_duplicates}")
    if num_duplicates > 0:
        report_lines.append("WARNING: Duplicates still exist!")
        report_lines.append(str(df[duplicates][['Refined_Formal_Name']].head()))
    else:
        report_lines.append("PASS: No duplicates found in 'Refined_Formal_Name'.")

    # 2. Analysis of Merged Fields
    # Check how many rows have merged content (indicated by '|')
    merged_entries = df['Original_Entry'].astype(str).str.contains(r'\|', regex=True).sum()
    merged_notes = df['Status/Notes'].astype(str).str.contains(r'\|', regex=True).sum()
    
    report_lines.append(f"\nEntries with merged variations (Original_Entry): {merged_entries} ({merged_entries/len(df)*100:.1f}%)")
    report_lines.append(f"Entries with merged notes (Status/Notes): {merged_notes} ({merged_notes/len(df)*100:.1f}%)")

    # 3. Sample of Merged Rows
    report_lines.append("\n=== Sample of Merged Rows ===")
    merged_df = df[df['Original_Entry'].astype(str).str.contains(r'\|', regex=True)]
    
    if not merged_df.empty:
        sample = merged_df.head(10)
        for idx, row in sample.iterrows():
            report_lines.append(f"\nName: {row['Refined_Formal_Name']}")
            report_lines.append(f"Original Entries: {row['Original_Entry']}")
            report_lines.append(f"Notes: {row['Status/Notes']}")
            report_lines.append("-" * 50)
    
    # 4. Category Distribution
    report_lines.append("\n=== Category Distribution ===")
    cat_counts = df['Refined_Category'].value_counts()
    for cat, count in cat_counts.items():
        report_lines.append(f"{cat}: {count}")

    # Write report
    with open(output_report, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print('\n'.join(report_lines))
    print(f"\nReport saved to {output_report}")

if __name__ == "__main__":
    analyze_deduplicated_data()
