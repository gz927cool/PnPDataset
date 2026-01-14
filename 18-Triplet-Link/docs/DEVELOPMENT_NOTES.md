# 项目开发总结与注意事项

本文档总结了知识图谱构建管线开发过程中遇到的关键问题、解决方案及后续维护的注意事项。

## 1. OpenAI 接口配置与兼容性

### 问题描述
在使用 OpenAI 兼容接口（非官方 OpenAI 服务）时，仅设置 `api_key` 是不够的，容易导致 `401 Unauthorized` 错误。

### 解决方案
必须在 `.env` 文件和配置类中同时明确以下三个参数：
- `OPENAI_API_KEY`: 认证密钥
- `OPENAI_BASE_URL`: 服务端点（如 `https://api.deepseek.com/v1`）
- `OPENAI_MODEL_NAME`: 明确指定模型名称（如 `deepseek-chat` 或 `gpt-4o`）

**代码实践**：
在 `src/services/llm.py` 中，初始化 Client 时必须显式传入 `base_url`：
```python
self._client = OpenAI(
    api_key=api_key, 
    base_url=config.OPENAI_BASE_URL
)
```

## 2. 断点续传与增量处理

### 问题描述
知识图谱构建涉及大量 API 调用（Wikidata, LLM），全量运行耗时且昂贵。程序崩溃或网络中断后，不能简单地从头开始。

### 解决方案
实现了基于文件状态的断点续传机制：

1.  **加载逻辑**：在 Step 3 (关系映射) 和 Step 4 (实体对齐) 启动时，先读取已生成的输出 CSV。
2.  **去重与校验**：
    *   **Step 3**: 按 `raw_relation` 维度去重加载，避免重复映射规则。
    *   **Step 4**: 仅跳过状态为 `accepted/rejected` 且备注中无 `Agent skipped`（降级标志）的记录。
3.  **错误重试**：对于 API 调用失败的记录（状态为 `error` 或未写入文件），下次运行时会自动重试。

## 3. 数据重复问题 (Step 3)

### 问题描述
`relations_mapping.csv` 文件曾出现大量重复数据。原因是：
1.  代码按“三元组”维度遍历，而非“关系类型”维度。
2.  断点续传加载时未对内存中的规则进行去重。

### 解决方案
*   **加载优化**：加载现有映射时使用 `drop_duplicates(subset=['raw_relation', 'mapped_property'])`。
*   **逻辑优化**：确保内存中维护的是“关系类型 -> Wikidata 属性”的唯一字典，生成文件时再展开到具体三元组。
*   **清洗脚本**：提供了 `src/utils/clean_relations.py` 用于清洗已污染的历史数据。

## 4. 缓存与持久化

### 问题描述
Wikidata 查询极其频繁，网络波动可能导致数据丢失。

### 解决方案
*   **自动保存**：在 `WikidataService` 中引入 `atexit` 模块，注册 `save` 函数，确保程序退出（包括异常退出）时自动将内存缓存写入磁盘。
*   **磁盘缓存**：所有查询结果持久化存储在 `data/wikidata_cache.json`。

## 5. LLM Agent 的降级与恢复

### 问题描述
初期为了测试流程跑通，在 Step 4 中使用了“降级策略”（Fallback），即跳过 LLM 直接选 Top 1 候选。这导致生成了大量低质量的 `Agent skipped` 记录。

### 解决方案
*   **智能识别**：在断点续传逻辑中，增加对 `notes` 字段的检查。如果发现包含 `Agent skipped`，则强制重新调用 LLM 进行处理。
*   **异常处理**：移除自动降级逻辑，遇到 LLM 错误时明确标记为 `error`，以便后续重试，保证数据质量。

## 6. 参数化运行

### 注意事项
`main.py` 和 `PipelineRunner` 支持命令行参数控制，便于调试：
*   `--steps`: 指定运行步骤（如 `0 2 3`）。
*   `--limit`: 限制处理数据量（如 `100`），用于快速验证代码逻辑。

```bash
# 示例：仅运行关系映射和对齐，限制前 50 条
python main.py --steps 3 4 --limit 50
```
