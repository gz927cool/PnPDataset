# 04-Index-Enrich 数据统计分析报告

**生成日期**: 2025-12-12 00:08:28

**总文件数**: 19
**总条目数**: 2930

## 1. 文件概览
| File               |   Rows |   Columns |
|:-------------------|-------:|----------:|
| A_refined.csv      |    155 |         9 |
| B_refined.csv      |    324 |         9 |
| C_refined.csv      |    432 |         9 |
| D_refined.csv      |     67 |         9 |
| E_refined.csv      |     21 |         9 |
| F_refined.csv      |    110 |         9 |
| G_refined.csv      |    196 |         9 |
| H_refined.csv      |     25 |         9 |
| I_refined.csv      |     11 |         9 |
| J，K_refined.csv   |     27 |         9 |
| L_refined.csv      |    121 |         9 |
| M_refined.csv      |    262 |         9 |
| N_refined.csv      |     46 |         9 |
| O_refined.csv      |     37 |         9 |
| P_refined.csv      |    276 |         9 |
| Q-R_refined.csv    |    240 |         9 |
| S_refined.csv      |    226 |         9 |
| T_refined.csv      |    128 |         9 |
| UVWXYZ_refined.csv |    226 |         9 |

## 2. 列数据完整性 (缺失值统计)
| Column             |   Missing Count |   Missing Percentage |   Filled Count |
|:-------------------|----------------:|---------------------:|---------------:|
| Index_Main Entry   |               0 |                 0    |           2930 |
| CIDOC_Type         |               0 |                 0    |           2930 |
| Index_Location     |            2770 |                94.54 |            160 |
| Proposed Location  |             735 |                25.09 |           2195 |
| 备注/来源          |             735 |                25.09 |           2195 |
| Index_Sub-entry    |            1379 |                47.06 |           1551 |
| Index_Detail       |            2855 |                97.44 |             75 |
| Index_Page Numbers |             111 |                 3.79 |           2819 |
| Source_File        |               0 |                 0    |           2930 |

## 3. CIDOC_Type 分布
| CIDOC_Type            |   Count |   Percentage |
|:----------------------|--------:|-------------:|
| E21 Person            |    2357 |        80.44 |
| E53 Place             |     280 |         9.56 |
| E22 Man-Made Object   |     146 |         4.98 |
| E74 Group             |      73 |         2.49 |
| E28 Conceptual Object |      54 |         1.84 |
| E5 Event              |      20 |         0.68 |

## 4. 地理位置分析

### Top 20 Proposed Locations
| Proposed Location      |   Count |
|:-----------------------|--------:|
| Rome                   |     622 |
| Venice                 |     533 |
| Europe                 |      94 |
| Florence               |      78 |
| London                 |      75 |
| Bologna                |      62 |
| Paris                  |      61 |
| Venice/Würzburg/Madrid |      55 |
| Naples                 |      55 |
| Venice/London          |      49 |
| Venice/Berlin          |      43 |
| Bologna/Rome           |      30 |
| Rome/Florence          |      28 |
| Rome/Paris             |      18 |
| Rome/Venice            |      17 |
| Naples/Florence/Madrid |      16 |
| Madrid                 |      15 |
| Rome/Naples            |      15 |
| Vienna                 |      11 |
| Ferrara                |      10 |

**唯一地点数量 (Proposed Location)**: 125

## 5. 主条目分析

**重复的主条目数**: 1848

(注意：这可能包含同名但不同义的条目，或者确实是重复)