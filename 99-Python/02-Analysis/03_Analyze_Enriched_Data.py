import pandas as pd
import os
import glob

def analyze_data():
    input_dir = r'c:\Users\001\Desktop\Github-Project\PnPDataset\04-Index-Enrich'
    output_dir = r'c:\Users\001\Desktop\Github-Project\PnPDataset\99-Python\02-Analysis'
    output_report = os.path.join(output_dir, 'Analysis_Report.md')
    
    all_files = glob.glob(os.path.join(input_dir, "*_refined.csv"))
    
    if not all_files:
        print("No refined CSV files found.")
        return

    df_list = []
    file_stats = []

    print(f"Found {len(all_files)} files. Reading...")

    for filename in all_files:
        try:
            df = pd.read_csv(filename)
            df['Source_File'] = os.path.basename(filename)
            df_list.append(df)
            file_stats.append({
                'File': os.path.basename(filename),
                'Rows': len(df),
                'Columns': len(df.columns)
            })
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    if not df_list:
        print("No data loaded.")
        return

    full_df = pd.concat(df_list, ignore_index=True)
    
    # --- Analysis ---
    
    report_lines = []
    report_lines.append("# 04-Index-Enrich 数据统计分析报告")
    report_lines.append(f"\n**生成日期**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"\n**总文件数**: {len(all_files)}")
    report_lines.append(f"**总条目数**: {len(full_df)}")
    
    # 1. File Statistics
    report_lines.append("\n## 1. 文件概览")
    stats_df = pd.DataFrame(file_stats)
    report_lines.append(stats_df.to_markdown(index=False))
    
    # 2. Column Statistics (Missing Values)
    report_lines.append("\n## 2. 列数据完整性 (缺失值统计)")
    missing_stats = full_df.isnull().sum().reset_index()
    missing_stats.columns = ['Column', 'Missing Count']
    missing_stats['Missing Percentage'] = (missing_stats['Missing Count'] / len(full_df) * 100).round(2)
    missing_stats['Filled Count'] = len(full_df) - missing_stats['Missing Count']
    report_lines.append(missing_stats.to_markdown(index=False))

    # 3. CIDOC_Type Distribution
    report_lines.append("\n## 3. CIDOC_Type 分布")
    if 'CIDOC_Type' in full_df.columns:
        type_counts = full_df['CIDOC_Type'].value_counts().reset_index()
        type_counts.columns = ['CIDOC_Type', 'Count']
        type_counts['Percentage'] = (type_counts['Count'] / len(full_df) * 100).round(2)
        report_lines.append(type_counts.to_markdown(index=False))
    else:
        report_lines.append("未找到 'CIDOC_Type' 列。")

    # 4. Location Analysis
    report_lines.append("\n## 4. 地理位置分析")
    if 'Proposed Location' in full_df.columns:
        loc_counts = full_df['Proposed Location'].value_counts().head(20).reset_index()
        loc_counts.columns = ['Proposed Location', 'Count']
        report_lines.append("\n### Top 20 Proposed Locations")
        report_lines.append(loc_counts.to_markdown(index=False))
        
        unique_locs = full_df['Proposed Location'].nunique()
        report_lines.append(f"\n**唯一地点数量 (Proposed Location)**: {unique_locs}")
    else:
        report_lines.append("未找到 'Proposed Location' 列。")

    # 5. Main Entry Analysis (Top Terms)
    report_lines.append("\n## 5. 主条目分析")
    if 'Index_Main Entry' in full_df.columns:
        # Check for duplicates
        dupes = full_df[full_df.duplicated(subset=['Index_Main Entry'], keep=False)]
        dupe_count = len(dupes)
        report_lines.append(f"\n**重复的主条目数**: {dupe_count}")
        if dupe_count > 0:
             report_lines.append("\n(注意：这可能包含同名但不同义的条目，或者确实是重复)")
    
    # Write Report
    with open(output_report, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"Analysis complete. Report saved to: {output_report}")
    print('\n'.join(report_lines)) # Also print to console for immediate feedback

if __name__ == "__main__":
    analyze_data()
