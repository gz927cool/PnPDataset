import pandas as pd
import os
import glob
from collections import Counter
import re

def analyze_content():
    input_dir = r'c:\Users\001\Desktop\Github-Project\PnPDataset\04-Index-Enrich'
    output_dir = r'c:\Users\001\Desktop\Github-Project\PnPDataset\99-Python\02-Analysis'
    output_report = os.path.join(output_dir, 'Content_Analysis_Report.md')
    
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
    report_lines.append("# 04-Index-Enrich 数据内容深度分析报告")
    report_lines.append(f"\n**生成日期**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. CIDOC Type Content Sampling
    report_lines.append("\n## 1. 各类型条目内容抽样")
    
    for cidoc_type in full_df['CIDOC_Type'].unique():
        subset = full_df[full_df['CIDOC_Type'] == cidoc_type]
        count = len(subset)
        report_lines.append(f"\n### {cidoc_type} (共 {count} 条)")
        
        # Sample 5 random entries
        sample = subset['Index_Main Entry'].sample(min(5, count), random_state=42).tolist()
        report_lines.append("**随机抽样**: " + ", ".join(sample))
        
        # If it's Man-Made Object, look for common words
        if cidoc_type == 'E22 Man-Made Object':
            words = []
            for entry in subset['Index_Main Entry'].dropna():
                words.extend(re.findall(r'\w+', entry.lower()))
            common_words = Counter(words).most_common(10)
            report_lines.append(f"**高频词**: {', '.join([f'{w}({c})' for w, c in common_words])}")

    # 2. Sub-entry Analysis
    report_lines.append("\n## 2. 子条目 (Sub-entry) 分析")
    sub_entries = full_df['Index_Sub-entry'].dropna()
    report_lines.append(f"**有子条目的记录数**: {len(sub_entries)}")
    
    # Common keywords in sub-entries
    sub_text = " ".join(sub_entries.astype(str))
    # Simple keyword extraction (ignoring common stop words roughly)
    words = re.findall(r'\b[a-zA-Z]{4,}\b', sub_text.lower())
    common_keywords = Counter(words).most_common(20)
    
    report_lines.append("\n### 子条目高频关键词 (Top 20)")
    report_lines.append("| Keyword | Count |")
    report_lines.append("| :--- | :--- |")
    for word, count in common_keywords:
        report_lines.append(f"| {word} | {count} |")

    # 3. Enrichment Analysis (备注/来源)
    report_lines.append("\n## 3. 增补信息 (备注/来源) 分析")
    enrichment = full_df['备注/来源'].dropna()
    report_lines.append(f"**包含增补信息的记录数**: {len(enrichment)}")
    
    # Check for Chinese characters to confirm translation
    chinese_count = enrichment.apply(lambda x: bool(re.search(r'[\u4e00-\u9fff]', str(x)))).sum()
    report_lines.append(f"**包含中文字符的记录数**: {chinese_count} (占比 {chinese_count/len(enrichment)*100:.1f}%)")
    
    # Sample enrichments
    report_lines.append("\n### 增补信息抽样")
    sample_enrich = enrichment.sample(min(5, len(enrichment)), random_state=42).tolist()
    for item in sample_enrich:
        report_lines.append(f"- {item}")

    # 4. Location vs Person Analysis
    report_lines.append("\n## 4. 地点与人物关联分析 (Top Locations)")
    
    top_locations = full_df['Proposed Location'].value_counts().head(5).index.tolist()
    
    for loc in top_locations:
        report_lines.append(f"\n### {loc}")
        loc_subset = full_df[full_df['Proposed Location'] == loc]
        
        # Who is associated with this location?
        people = loc_subset[loc_subset['CIDOC_Type'] == 'E21 Person']['Index_Main Entry']
        people_count = len(people)
        report_lines.append(f"**相关人物数量**: {people_count}")
        if people_count > 0:
            report_lines.append(f"**人物示例**: {', '.join(people.sample(min(5, people_count), random_state=42).tolist())}")
            
        # What groups are associated?
        groups = loc_subset[loc_subset['CIDOC_Type'] == 'E74 Group']['Index_Main Entry']
        if len(groups) > 0:
             report_lines.append(f"**相关机构/团体**: {', '.join(groups.tolist())}")

    # Write Report
    with open(output_report, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"Content analysis complete. Report saved to: {output_report}")
    print('\n'.join(report_lines))

if __name__ == "__main__":
    analyze_content()
