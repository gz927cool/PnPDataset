# PnP Dataset Processing Scripts

此文件夹包含用于处理、分析和丰富 PnP 数据集的所有 Python 脚本。脚本按功能分为三个主要阶段。

## 📂 01-Process (数据处理流水线)
此文件夹包含核心的数据清洗和转换脚本。建议按顺序运行。

| 脚本名 | 功能描述 |
| :--- | :--- |
| `01_Apply_Initial_CIDOC.py` | 初步应用 CIDOC CRM 类型分类 (E21, E53 等)。 |
| `02_Update_Specific_Unknowns.py` | 更新特定的未知类型条目。 |
| `03_Finalize_Unknown_Classification.py` | 完成剩余未知条目的分类。 |
| `04_Fix_Quoted_Terms.py` | 修复被错误引用的术语格式。 |
| `05_Fix_Type_Mismatches.py` | 修复类型不匹配的数据错误。 |
| `06_Rename_Columns.py` | 标准化列名 (如 Index_Main Entry)。 |
| `07_Preview_Location_Enrichment.py` | 预览地点数据的丰富效果。 |
| `08_Add_Location_Columns.py` | 添加地点相关的空列 (Proposed Location 等)。 |
| `09_Update_Location_Chinese_Notes.py` | 更新地点的中文备注信息。 |
| `10_Enrich_All_Locations.py` | 对所有文件执行地点丰富化操作。 |
| `11_Organize_Workspace.py` | (工具) 整理工作区文件夹结构。 |
| `12_Generate_Crosscheck_Files.py` | 生成用于与人工数据对比的中间文件 (`_crosscheck.csv`)。 |

## 📂 02-Analysis (统计与对比分析)
此文件夹包含用于生成报告和对比不同数据集的脚本。

| 脚本名 | 功能描述 |
| :--- | :--- |
| `01_Audit_Missing_Locations.py` | 审计缺失地点信息的条目。 |
| `02_Analyze_Missing.py` | 分析缺失数据的模式。 |
| `03_Analyze_Enriched_Data.py` | 对丰富后的数据进行统计分析。 |
| `04_Analyze_Content_Details.py` | 分析索引内容的详细信息。 |
| `05_Deep_Entity_Analysis.py` | 深度实体分析 (去重、频率统计)。 |
| `06_Compare_Datasets.py` | (基础) 对比索引数据(04)与人工数据(05)。 |
| `07_Normalize_and_Match.py` | (高级) 使用归一化策略进行深度匹配。 |
| `08_Generate_Consolidated_Report.py` | 生成简单的合并对比报告。 |
| `09_Generate_Full_Comparison_Report.py` | 生成完整的对比矩阵 (包含未匹配的人工数据)。 |

**生成的报告:**
- `Analysis_Report.md`: 总体数据分析报告。
- `Data_Comparison_Report.md`: 基础对比报告。
- `Advanced_Comparison_Report.md`: 高级归一化对比报告。

## 📂 03-Getty-Integration (Getty 数据集成)
此文件夹包含用于查询本地 Getty Vocabularies (ULAN, TGN, AAT) 的工具。

| 脚本名 | 功能描述 |
| :--- | :--- |
| `01_Query_Local_Getty_ULAN.py` | 扫描本地 ULAN `.nt` 文件以查找匹配项。 |
| `02_Get_Hogarth_Details.py` | (示例) 获取特定艺术家 (Hogarth) 的详细信息。 |
| `03_Get_ScopeNote.py` | 从 RDF 数据中提取 ScopeNote (传记/描述)。 |
| `04_Query_Getty_B_Full.py` | 对 `B_refined.csv` 执行完整的 Getty 查询 (ULAN/TGN/AAT)。 |
| `05_Query_Getty_B_Sample.py` | 对 `B_refined.csv` 执行小样本测试查询。 |

## 📂 Archive (归档)
包含旧的 `StepX` 系列脚本和失败的 API 尝试脚本。仅供参考。
