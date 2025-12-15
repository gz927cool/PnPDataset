import pandas as pd
import os
import glob

def analyze_entities():
    input_dir = r'c:\Users\001\Desktop\Github-Project\PnPDataset\04-Index-Enrich'
    output_dir = r'c:\Users\001\Desktop\Github-Project\PnPDataset\99-Python\02-Analysis'
    output_report = os.path.join(output_dir, 'Entity_Analysis_Report.md')
    
    all_files = glob.glob(os.path.join(input_dir, "*_refined.csv"))
    
    df_list = []
    for filename in all_files:
        try:
            df = pd.read_csv(filename)
            df_list.append(df)
        except:
            pass

    if not df_list:
        print("No data found.")
        return

    full_df = pd.concat(df_list, ignore_index=True)
    
    report_lines = []
    report_lines.append("# 04-Index-Enrich 实体深度分析报告 (去重统计)")
    report_lines.append(f"\n**生成日期**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    total_rows = len(full_df)
    unique_entities = full_df['Index_Main Entry'].nunique()
    
    report_lines.append("\n## 1. 总体统计")
    report_lines.append(f"- **总记录数 (Total Rows)**: {total_rows}")
    report_lines.append(f"- **去重后实体总数 (Unique Entities)**: {unique_entities}")
    report_lines.append(f"- **总体重复率**: {(1 - unique_entities/total_rows)*100:.2f}%")

    report_lines.append("\n## 2. 按类型 (CIDOC_Type) 统计")
    
    type_stats = []
    for c_type in full_df['CIDOC_Type'].unique():
        subset = full_df[full_df['CIDOC_Type'] == c_type]
        n_rows = len(subset)
        n_unique = subset['Index_Main Entry'].nunique()
        type_stats.append({
            'CIDOC_Type': c_type,
            'Total Records': n_rows,
            'Unique Entities': n_unique,
            'Avg Records per Entity': round(n_rows / n_unique, 2)
        })
    
    stats_df = pd.DataFrame(type_stats).sort_values('Total Records', ascending=False)
    report_lines.append(stats_df.to_markdown(index=False))

    report_lines.append("\n## 3. 高频实体 (Top 20)")
    report_lines.append("这些实体在索引中出现了多次（可能在不同页面被引用）。")
    
    top_entities = full_df['Index_Main Entry'].value_counts().head(20).reset_index()
    top_entities.columns = ['Entity', 'Frequency']
    # Join with Type to show what they are
    # We take the first type found for each entity (assuming consistency)
    entity_types = full_df[['Index_Main Entry', 'CIDOC_Type']].drop_duplicates('Index_Main Entry')
    top_entities = top_entities.merge(entity_types, left_on='Entity', right_on='Index_Main Entry', how='left')
    top_entities = top_entities[['Entity', 'CIDOC_Type', 'Frequency']]
    
    report_lines.append(top_entities.to_markdown(index=False))

    report_lines.append("\n## 4. 数据一致性检查")
    # Check if any entity has multiple different CIDOC Types
    type_consistency = full_df.groupby('Index_Main Entry')['CIDOC_Type'].nunique()
    inconsistent_entities = type_consistency[type_consistency > 1]
    
    if len(inconsistent_entities) > 0:
        report_lines.append(f"\n**发现 {len(inconsistent_entities)} 个实体具有多种类型分类**:")
        for entity in inconsistent_entities.index:
            types = full_df[full_df['Index_Main Entry'] == entity]['CIDOC_Type'].unique()
            report_lines.append(f"- **{entity}**: {', '.join(types)}")
    else:
        report_lines.append("\n所有实体的类型分类一致 (没有发现同一实体被标记为不同类型的情况)。")

    # Write Report
    with open(output_report, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"Entity analysis complete. Report saved to: {output_report}")
    print('\n'.join(report_lines))

if __name__ == "__main__":
    analyze_entities()
