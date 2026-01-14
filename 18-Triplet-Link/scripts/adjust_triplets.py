#!/usr/bin/env python3
"""
调整 extracted_triplets.csv，基于 _source_file 和 Row_ID 构建 Row_Index，
格式对齐 merged_index_enrich.csv 中的 index（如 A_1, B_12）
"""

import os
import re
import pandas as pd
from pathlib import Path

SOURCE_FILE = Path(__file__).parent / "extracted_triplets.csv"
OUTPUT_FILE = Path(__file__).parent / "extracted_triplets_adj.csv"


def extract_letter_from_source(source_file: str) -> str:
    """从源文件名提取字母标识（如 '01-A 深度解析全量结果表 (1-100行).md' -> 'A'）"""
    # 匹配 01-A, 02-B 等格式
    match = re.search(r'\d{2}-([A-Z])', source_file)
    if match:
        return match.group(1)
    # 处理 J，K 这种特殊情况
    match = re.search(r'\d{2}-([A-Z，]+)', source_file)
    if match:
        return match.group(1)
    return "Unknown"


def main():
    # 读取 CSV
    df = pd.read_csv(SOURCE_FILE, encoding="utf-8-sig")
    print(f"读取文件: {len(df)} 行")

    # 检查必需列
    if "_source_file" not in df.columns or "Row_ID" not in df.columns:
        print("错误: 缺少必需列 _source_file 或 Row_ID")
        return

    # 构建 Row_Index 列
    df["Row_Index"] = df.apply(
        lambda row: f"{extract_letter_from_source(row['_source_file'])}_{row['Row_ID']}",
        axis=1
    )

    # 排除 _source_file 和 Row_ID 列
    exclude_cols = ["_source_file", "Row_ID"]
    cols = ["Row_Index"] + [c for c in df.columns if c != "Row_Index" and c not in exclude_cols]
    df = df[cols]

    # 保存结果
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"保存文件: {OUTPUT_FILE}")
    print(f"总行数: {len(df)}")
    print(f"\n前10行预览:")
    print(df[["Row_Index", "主体 (Subject)", "谓词 (Predicate)", "客体 (Object)"]].head(10).to_string())


if __name__ == "__main__":
    main()
