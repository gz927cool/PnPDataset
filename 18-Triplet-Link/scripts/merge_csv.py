#!/usr/bin/env python3
"""
合并 01-Index-Enrich 目录下的所有 CSV 文件，
新增 index 列，值为 文件名_行号 格式
"""

import os
import pandas as pd
from pathlib import Path

# 目录路径
SOURCE_DIR = Path(__file__).parent
OUTPUT_FILE = SOURCE_DIR / "merged_index_enrich.csv"


def extract_base_name(filename: str) -> str:
    """从文件名提取基础名称（去掉 _refined.csv 后缀）"""
    return filename.replace("_refined.csv", "")


def merge_csv_files():
    """合并所有 CSV 文件并添加 index 列"""
    all_dataframes = []

    csv_files = sorted(SOURCE_DIR.glob("*_refined.csv"))

    print(f"找到 {len(csv_files)} 个 CSV 文件")

    for csv_file in csv_files:
        base_name = extract_base_name(csv_file.name)

        # 读取 CSV，跳过空行
        df = pd.read_csv(csv_file, skip_blank_lines=True)

        # 检查是否为空 DataFrame
        if df.empty:
            print(f"  跳过空文件: {csv_file.name}")
            continue

        # 获取行数（数据行，不含表头）
        num_rows = len(df)

        # 生成 index 列：文件名_行号（行号从1开始）
        # 使用枚举时 +1 表示行号从1开始
        index_values = [f"{base_name}_{i+1}" for i in range(num_rows)]

        # 在第一列前插入 index 列
        df.insert(0, "index", index_values)

        all_dataframes.append(df)
        print(f"  已处理: {csv_file.name} - {num_rows} 行")

    if not all_dataframes:
        print("没有有效数据可合并")
        return

    # 合并所有 DataFrame
    merged_df = pd.concat(all_dataframes, ignore_index=True)

    # 保存结果
    merged_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"\n合并完成: {OUTPUT_FILE}")
    print(f"总行数: {len(merged_df)}")
    print(f"列名: {list(merged_df.columns)}")


if __name__ == "__main__":
    merge_csv_files()
