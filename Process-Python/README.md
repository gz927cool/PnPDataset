# PnP Dataset Processing Documentation

本文档是 PnP 数据集处理项目的核心文档，详细记录了从原始数据清洗、对比、外部丰富到最终合并的全流程。所有脚本均位于 `Process-Python` 文件夹中。

---

## 📂 1. 数据集目录结构 (Directory Structure)

*   **`04-Index-Enrich`**: 机器提取并经过初步清洗的索引数据。
*   **`05-HandmadeDataset`**: 人工整理的高质量数据表。
*   **`06-Crosscheck`**: 对比分析过程中的中间文件（审计列表、匹配矩阵）。
*   **`07-MML`**: 人工/大模型辅助校验的分块数据。
*   **`08-EntityMerge`**: **最终合并的数据集**（包含去重后的实体）。
*   **`08-Recheck`**: 待复核数据的合并集。
*   **`Process-Python`**: 所有处理脚本及本文档。

---

## 🚀 2. 处理流水线 (Processing Pipeline)

整个数据处理工作流按逻辑顺序分为以下五个阶段：

### 阶段一：基础清洗与准备 (Initial Processing)
*   **目标**: 对原始 PDF 提取的数据进行类型分类、格式修复和地点丰富。
*   **脚本**: `01` - `09` 系列脚本 (位于 `01-Process` 子文件夹)。
*   **关键产出**: `04-Index-Enrich` 中的 `*_refined.csv` 文件。

### 阶段二：交叉对比与审计 (Cross-check & Audit)
*   **目标**: 将机器数据 (Index) 与人工数据 (Manual) 进行全量对比，识别差异。
*   **脚本**:
    *   `10_Deduplicate_Matrix.py`: 生成全量对比矩阵。
    *   `12_Extract_Manual_Audit.py`: 提取未匹配的“问题数据”。
*   **关键产出**:
    *   `06-Crosscheck/Full_Comparison_Matrix_Unique.csv`: 全量对比母版。
    *   `06-Crosscheck/Audit_List_Combined.csv`: 待审计列表 (1610条)。

### 阶段三：深度标准化与外部链接 (Normalization & Enrichment)
*   **目标**: 清洗历史名称格式，并链接 Wikidata 获取 QID。
*   **脚本**:
    *   `14_Normalize_Audit_List_Full.py`: 深度清洗人名/地名/作品名。
    *   `15_Query_Wikidata.py`: 调用 Wikidata API 进行匹配。
    *   `17_Refine_Wikidata_Matches.py`: 自动采纳高置信度匹配。
*   **关键产出**:
    *   `06-Crosscheck/Audit_List_Wikidata_Refined.csv`: 包含 QID 的精炼列表。

### 阶段四：全量合并与去重 (Final Merge & Deduplication)
*   **目标**: 将 Index 和 Manual 数据集物理合并，并基于对比结果进行去重。
*   **脚本**:
    *   `18_Merge_All_Datasets.py`: 合并 `04` 和 `05` 文件夹的所有数据。
    *   `19_Deduplicate_Merged_Entity.py`: 利用 `06` 中的映射关系进行去重。
    *   `20_Create_Simplified_Dataset.py`: 生成带序号的简化版最终表。
*   **关键产出**:
    *   `08-EntityMerge/01-Merged_All_Entities.csv`: 原始合并表 (6315行)。
    *   `08-EntityMerge/02-Deduplicated_Entities.csv`: 去重后全表 (4116行)。
    *   `08-EntityMerge/03-Simplified_Entities.csv`: **最终交付表** (含 ID, Name, Type, Files)。

### 阶段五：复核数据整合 (Recheck Consolidation)
*   **目标**: 将分散在 `07-MML` 中的人工校验文件合并。
*   **脚本**:
    *   `21_Merge_Recheck_Files.py`: 扫描并合并所有分块 CSV。
*   **关键产出**:
    *   `08-Recheck/01-Merged_Recheck.csv`: 合并后的复核数据 (4118行)。

---

## 📊 3. 关键统计结果 (Key Statistics)

### 3.1 最终实体库 (Entity Merge)
*   **原始合并总数**: 6315 条
*   **去重后总数**: **4116 条**
*   **数据来源分布**:
    *   Handmade (人工): ~54%
    *   Index (机器): ~46%
*   **实体类型分布**:
    *   Person (人物): ~68%
    *   Place (地点): ~16%
    *   Object/Work (作品): ~14%

### 3.2 Wikidata 匹配情况 (Audit List)
针对 1610 条疑难数据的匹配结果：
*   **成功匹配**: 731 条 (45.4%)
*   **未匹配**: 879 条 (54.6%)

---

## 📜 4. 脚本索引 (Script Index)

| 脚本名 | 功能描述 | 阶段 |
| :--- | :--- | :--- |
| `10_Deduplicate_Matrix.py` | 生成对比矩阵 | Cross-check |
| `14_Normalize_Audit_List_Full.py` | 名称标准化 | Enrichment |
| `15_Query_Wikidata.py` | Wikidata 查询 | Enrichment |
| `16_Analyze_Wikidata_Results.py` | 结果分析统计 | Analysis |
| `17_Refine_Wikidata_Matches.py` | 自动精炼匹配 | Enrichment |
| `18_Merge_All_Datasets.py` | 数据集物理合并 | Final Merge |
| `19_Deduplicate_Merged_Entity.py` | 实体去重 | Final Merge |
| `20_Create_Simplified_Dataset.py` | 生成简化交付表 | Final Merge |
| `21_Merge_Recheck_Files.py` | 合并复核文件 | Recheck |

---

*Last Updated: 2025-12-15*

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
