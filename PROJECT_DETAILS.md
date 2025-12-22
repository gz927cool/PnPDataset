# PnPDataset 项目详细技术说明与操作指南

## 1. 项目背景 (Project Background)
本项目名为 **PnPDataset** (Patrons and Painters Dataset)，主要目标是数字化、清洗并结构化 Francis Haskell 的经典艺术史著作《Patrons and Painters》中的索引数据。该书记录了17-18世纪意大利及欧洲其他地区的艺术赞助人与画家之间的关系。

## 2. 数据流转说明 (Data Flow)

### 2.1 从原始书籍到初步索引
1.  **PDF (00-book/)**: 原始扫描件。
2.  **Markdown (02-Markdown/)**: 通过 OCR 或转换得到的章节文本，用于上下文校验。
3.  **CSV (03-Index/)**: 从索引页解析出的原始条目，包含：
    *   `Main Entry`: 索引主条目。
    *   `Type`: 原始分类（通常不准确）。
    *   `Location`: 条目所在的页码或章节。

### 2.2 LLM 语义增强 (06-LLM-Enhancement/)
使用 Google Gemini 1.5 Pro 对原始 CSV 进行 100 行/批次的增强处理：
- **OCR 修复**: 自动修复如 `Orl谷ans` -> `Orléans` 的乱码。
- **分类重构**: 基于 CIDOC-CRM 标准将实体重新划分为：
    *   `Person`: 人物（如画家、赞助人）。
    *   `Work`: 艺术作品（如绘画、雕塑）。
    *   `Place`: 地理位置、建筑。
    *   `Organization`: 学院、修会。
    *   `Concept`: 艺术史概念。
- **实体消歧**: 区分同名人物，识别家族关系。

### 2.3 最终验证与 QID 链接 (08-QID-Crosscheck/)
通过 Python 脚本与 Wikidata API 交互，为实体匹配唯一的 **QID**，确保数据的全球唯一性与可链接性。

## 3. 文件夹详细说明 (Folder Details)

| 文件夹 | 详细内容 | 作用 |
| :--- | :--- | :--- |
| `00-book/` | 各章节 PDF 文件 | 原始参考文献 |
| `03-Index/` | 按字母分类的 MD/CSV/PDF | 索引处理的核心工作区 |
| `04-HandmadeDataset/` | 人工维护的 3 个 CSV 表 | 黄金标准参考集 (Golden Dataset) |
| `05-EntityMerge/` | 合并后的中间 CSV | 消除跨章节重复条目 |
| `06-LLM-Enhancement/` | LLM 输出结果 + 技术报告 | 数据质量的质变阶段 |
| `07-Data-Remerge/` | 重聚合后的全量表 | QID 匹配前的最终底表 |
| `08-QID-Crosscheck/` | 最终清洗版 + QID | **最终交付成果** |
| `Process-Python/` | 自动化脚本工具链 | 支撑整个流程的自动化逻辑 |

## 4. 自动化处理步骤 (Operational Steps)

### 第一阶段：数据准备
- 运行 `03-Index/` 相关的提取逻辑（若需重新从 PDF 提取）。
- 准备好 `04-HandmadeDataset/` 中的人工参考表。

### 第二阶段：Python 脚本流水线 (01-Process/)
按文件名编号顺序执行：
1.  **`01_Apply_Initial_CIDOC.py`**: 初始化实体分类。
2.  **`02` - `05`**: 逐步修复未知类型、引号问题、分类错误。
3.  **`06_Rename_Columns.py`**: 统一字段命名规范。
4.  **`07` - `10`**: 地理位置数据的批量翻译与中文备注增强。
5.  **`11_Organize_Workspace.py`**: 自动整理文件结构。
6.  **`12_Generate_Crosscheck_Files.py`**: 生成审计报告，检查与人工表的匹配度。

### 第三阶段：结果产出
- 核心产出文件：`08-QID-Crosscheck/02-Merged_Recheck_With_QID_Cleaned.csv`
- 使用 Excel 打开 `07-Data-Remerge/04-Merged_Recheck_With_QID.xlsx` 进行最后的人工抽检。

## 5. 技术依赖
- **Python 3.10+**
- **Libraries**: `pandas`, `openpyxl`, `re`, `glob`
- **LLM**: Gemini 1.5 Pro (via API)
