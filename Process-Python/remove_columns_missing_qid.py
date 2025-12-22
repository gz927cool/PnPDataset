import pandas as pd

# 读取CSV文件
input_path = r'c:\Users\001\Desktop\Github-Project\PnPDataset\09-QID-Crosscheck\05-Missing_QID_Report_Filled.csv'
df = pd.read_csv(input_path)

# 要删除的列
cols_to_drop = [
    'Original-Status/Notes',
    'Second-Query_Label',
    'Second-Query_Description',
    'Second-Query_Logic'
]

# 删除列
new_df = df.drop(columns=cols_to_drop, errors='ignore')

# 保存到新文件（可覆盖原文件或另存为新文件）
output_path = input_path  # 如需备份可改为新文件名
new_df.to_csv(output_path, index=False, encoding='utf-8-sig')
print('指定列已删除并保存。')
