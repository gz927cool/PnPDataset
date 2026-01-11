#!/usr/bin/env python3
"""
从16-Index-Triplet目录下的md文件中提取全量原子化解析结果表
"""

import re
import os
from pathlib import Path
from typing import List, Dict, Optional
import csv


def extract_table_from_md(md_content: str) -> List[Dict]:
    """
    从md内容中提取全量原子化解析结果表
    支持两种格式:
    1. A类型: 包含 "三、 全量原子化解析结果表" 章节，有 Index 列
    2. B类型: 直接是表格，列顺序为 序号, 主体, 谓词, 客体, 状态, 深度核验逻辑, Row ID

    注意：只提取"二、全量原子化解析结果表"或"三、全量原子化解析结果表"章节下的数据
    不提取后续的"无匹配/已过滤行汇总"等章节
    """
    results = []

    # 检查是否是A类型（有 "全量原子化解析结果表" 章节）
    # 支持 "二、" 和 "三、" 两种编号
    section_pattern = r'## \*\*[二三][、\s]*全量原子化解析结果表[^\n]*\n'
    section_match = re.search(section_pattern, md_content)

    if section_match:
        # A/C类型: 使用章节后直接解析表格的逻辑
        section_start = section_match.end()

        # 找到下一个章节标题的位置，限制解析范围
        next_section_pattern = r'\n## \*\*[一二三四五六七八九十]+[、\s]'
        next_section_match = re.search(next_section_pattern, md_content[section_start:])

        if next_section_match:
            section_end = section_start + next_section_match.start()
        else:
            section_end = len(md_content)

        lines = md_content[section_start:section_end].split('\n')

        # 查找表头行（包含 Index 或 序号）
        header_idx = -1
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('|') and ('Index' in stripped or '序号' in stripped):
                header_idx = i
                break

        if header_idx < 0:
            return []

        # 解析表头
        header_line = lines[header_idx].strip()
        headers = [h.strip() for h in header_line.strip('|').split('|')]

        # 构建列名映射（统一到标准名称）
        column_mapping = {}
        for i, h in enumerate(headers):
            h_lower = h.lower().strip()
            if '序号' in h or 'index' in h_lower:
                column_mapping[i] = 'Index'
            elif 'row id' in h_lower:
                column_mapping[i] = 'Row ID'
            elif '主体' in h or 'subject' in h_lower:
                column_mapping[i] = '主体 (Subject)'
            elif '谓词' in h or 'predicate' in h_lower:
                column_mapping[i] = '谓词 (Predicate)'
            elif '客体' in h or 'object' in h_lower:
                column_mapping[i] = '客体 (Object)'
            elif '状态' in h or 'status' in h_lower:
                column_mapping[i] = '状态 (Status)'
            elif '依据' in h or 'source' in h_lower:
                column_mapping[i] = '依据 (Source)'
            elif '核验' in h or 'evidence' in h_lower or 'logic' in h_lower:
                column_mapping[i] = '核验逻辑 (Evidence_Logic)'

        # 跳过表头和分隔线
        data_start = header_idx + 1
        if data_start < len(lines) and '---' in lines[data_start]:
            data_start += 1

        # 解析数据行
        for i in range(data_start, len(lines)):
            line = lines[i].strip()
            # 跳过空行、非表格行、表头分隔行
            if not line or not line.startswith('|'):
                if line and not line.startswith('#'):
                    break
                continue
            # 跳过表头分隔行 (如 | :---- | :---- | ...)
            if ':----' in line or '---' in line:
                continue

            cells = [c.strip() for c in line.strip('|').split('|')]

            if len(cells) >= 3:
                row_data = {}
                for j, cell in enumerate(cells):
                    if j in column_mapping:
                        row_data[column_mapping[j]] = cell

                if row_data.get('Index', '').strip() or row_data.get('主体 (Subject)', '').strip():
                    results.append(row_data)

    else:
        # B类型: 直接查找表格，表头包含 "序号" 或 "主体 (Subject)"
        all_lines = md_content.split('\n')
        header_idx = -1

        for i, line in enumerate(all_lines):
            stripped = line.strip()
            if stripped.startswith('|') and ('序号' in stripped or '主体 (Subject)' in stripped):
                header_idx = i
                break

        if header_idx < 0:
            return []

        # 解析表头
        header_line = all_lines[header_idx].strip()
        headers = [h.strip() for h in header_line.strip('|').split('|')]

        # 标准化列名映射
        column_mapping = {}
        for i, h in enumerate(headers):
            h_lower = h.lower().strip()
            if '序号' in h or 'index' in h_lower:
                column_mapping[i] = 'Index'
            elif 'row id' in h_lower:
                column_mapping[i] = 'Row ID'
            elif '主体' in h or 'subject' in h_lower:
                column_mapping[i] = '主体 (Subject)'
            elif '谓词' in h or 'predicate' in h_lower:
                column_mapping[i] = '谓词 (Predicate)'
            elif '客体' in h or 'object' in h_lower:
                column_mapping[i] = '客体 (Object)'
            elif '状态' in h or 'status' in h_lower:
                column_mapping[i] = '状态 (Status)'
            elif '依据' in h or 'source' in h_lower:
                column_mapping[i] = '依据 (Source)'
            elif '核验' in h or 'evidence' in h_lower or 'logic' in h_lower:
                column_mapping[i] = '核验逻辑 (Evidence_Logic)'

        # 跳过表头和分隔线
        data_start = header_idx + 1
        if data_start < len(all_lines) and '---' in all_lines[data_start]:
            data_start += 1

        # 解析数据行
        for i in range(data_start, len(all_lines)):
            line = all_lines[i].strip()
            # 跳过空行、非表格行、表头分隔行
            if not line or not line.startswith('|'):
                if line and not line.startswith('#'):
                    break
                continue
            # 跳过表头分隔行 (如 | :---- | :---- | ...)
            if ':----' in line or '---' in line:
                continue

            cells = [c.strip() for c in line.strip('|').split('|')]

            if len(cells) >= 3:  # 至少需要主体、谓词、客体
                row_data = {}
                for j, cell in enumerate(cells):
                    if j in column_mapping:
                        row_data[column_mapping[j]] = cell

                # 标准化 Row ID 列
                if 'Row ID' not in row_data and 'Index' in row_data:
                    # 如果没有 Row ID 列，尝试从 Index 提取
                    pass

                # 确保有主体和谓词才添加
                if row_data.get('主体 (Subject)', '').strip():
                    results.append(row_data)

    return results


def extract_section_content(md_content: str, section_title: str) -> str:
    """
    提取指定章节的完整内容
    """
    # 转义特殊字符用于正则
    escaped_title = re.escape(section_title)

    # 匹配章节标题到下一个章节或文件末尾
    pattern = rf'## \*\*[一二三]+、\s*{escaped_title}.*?(?=\n## \*\*|\Z)'
    match = re.search(pattern, md_content, re.DOTALL)

    if match:
        return match.group(0)
    return ''


def process_md_file(file_path: str) -> List[Dict]:
    """
    处理单个md文件，提取结果表
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return extract_table_from_md(content)


def get_all_md_files(directory: str) -> List[str]:
    """
    获取目录下所有md文件
    """
    md_files = []
    for root, _, files in os.walk(directory):
        for file in sorted(files):
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return sorted(md_files)


def extract_index_range(filename: str) -> tuple:
    """
    从文件名中提取索引范围
    """
    # 匹配 (数字-数字) 格式
    pattern = r'\((\d+)-(\d+)行\)'
    match = re.search(pattern, filename)
    if match:
        return int(match.group(1)), int(match.group(2))
    return 0, 0


def save_to_csv(data: List[Dict], output_path: str):
    """
    保存数据到CSV文件
    """
    if not data:
        print("没有数据可保存")
        return

    # 获取所有列名
    all_keys = set()
    for row in data:
        all_keys.update(row.keys())

    # 按固定顺序排列列
    preferred_order = [
        'Index', 'Row ID', '主体 (Subject)', '谓词 (Predicate)',
        '客体 (Object)', '状态 (Status)', '依据 (Source)', '核验逻辑 (Evidence_Logic)'
    ]
    headers = preferred_order + [k for k in all_keys if k not in preferred_order]

    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)

    print(f"已保存 {len(data)} 条记录到 {output_path}")


def save_to_json(data: List[Dict], output_path: str):
    """
    保存数据到JSON文件
    """
    import json

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"已保存 {len(data)} 条记录到 {output_path}")


def main():
    """
    主函数
    """
    # 设置目录路径 - 脚本所在目录的父目录
    base_dir = Path(__file__).parent

    if not base_dir.exists():
        print(f"目录不存在: {base_dir}")
        return

    # 获取所有md文件
    md_files = get_all_md_files(str(base_dir))

    if not md_files:
        print("未找到md文件")
        return

    print(f"找到 {len(md_files)} 个md文件")

    # 收集所有数据
    all_data = []
    file_stats = []

    for file_path in md_files:
        filename = os.path.basename(file_path)
        data = process_md_file(file_path)

        # 提取索引范围用于排序
        idx_range = extract_index_range(filename)

        file_stats.append({
            'filename': filename,
            'count': len(data),
            'range': idx_range
        })

        for row in data:
            row['_source_file'] = filename
            all_data.append(row)

        print(f"  {filename}: {len(data)} 条记录")

    # 按文件名排序（这通常会按字母顺序，包含索引范围）
    all_data.sort(key=lambda x: (x.get('_source_file', ''), x.get('Index', '')))

    # 保存结果
    output_dir = base_dir / 'output'
    output_dir.mkdir(exist_ok=True)

    # 保存CSV
    csv_path = output_dir / 'extracted_triplets.csv'
    save_to_csv(all_data, str(csv_path))

    # 保存JSON
    json_path = output_dir / 'extracted_triplets.json'
    save_to_json(all_data, str(json_path))

    # 输出统计摘要
    print("\n=== 统计摘要 ===")
    print(f"总记录数: {len(all_data)}")

    # 统计唯一主体、谓词、客体
    subjects = set()
    predicates = set()
    objects = set()

    for row in all_data:
        if '主体 (Subject)' in row:
            subjects.add(row['主体 (Subject)'])
        if '谓词 (Predicate)' in row:
            predicates.add(row['谓词 (Predicate)'])
        if '客体 (Object)' in row:
            objects.add(row['客体 (Object)'])

    print(f"唯一主体数: {len(subjects)}")
    print(f"唯一谓词数: {len(predicates)}")
    print(f"唯一客体数: {len(objects)}")

    # 谓词统计
    print("\n谓词分布:")
    pred_counts = {}
    for row in all_data:
        pred = row.get('谓词 (Predicate)', '')
        pred_counts[pred] = pred_counts.get(pred, 0) + 1

    for pred, count in sorted(pred_counts.items(), key=lambda x: -x[1])[:15]:
        print(f"  {pred}: {count}")


if __name__ == '__main__':
    main()
