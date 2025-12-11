# 04-Index-Enrich 实体深度分析报告 (去重统计)

**生成日期**: 2025-12-12 00:16:30

## 1. 总体统计
- **总记录数 (Total Rows)**: 2930
- **去重后实体总数 (Unique Entities)**: 1432
- **总体重复率**: 51.13%

## 2. 按类型 (CIDOC_Type) 统计
| CIDOC_Type            |   Total Records |   Unique Entities |   Avg Records per Entity |
|:----------------------|----------------:|------------------:|-------------------------:|
| E21 Person            |            2357 |              1160 |                     2.03 |
| E53 Place             |             280 |               109 |                     2.57 |
| E22 Man-Made Object   |             146 |                69 |                     2.12 |
| E74 Group             |              73 |                50 |                     1.46 |
| E28 Conceptual Object |              54 |                35 |                     1.54 |
| E5 Event              |              20 |                 9 |                     2.22 |

## 3. 高频实体 (Top 20)
这些实体在索引中出现了多次（可能在不同页面被引用）。
| Entity                                 | CIDOC_Type          |   Frequency |
|:---------------------------------------|:--------------------|------------:|
| Churches                               | E22 Man-Made Object |          63 |
| Tiepolo, Giambattista                  | E21 Person          |          55 |
| Poussin, Nicolas                       | E21 Person          |          47 |
| Bernini, Gian Lorenzo                  | E21 Person          |          44 |
| Algarotti, Francesco                   | E53 Place           |          43 |
| Smith, Joseph                          | E21 Person          |          37 |
| Ricci, Sebastiano                      | E21 Person          |          33 |
| Venice                                 | E53 Place           |          31 |
| Canaletto                              | E21 Person          |          31 |
| Barberini, Maffeo (Pope Urban VIII)    | E21 Person          |          29 |
| Berrettini, Pietro (Pietro da Cortona) | E21 Person          |          25 |
| Piazzetta, Giovanni Battista           | E21 Person          |          24 |
| Rosa, Salvator                         | E21 Person          |          23 |
| Claude Lorrain                         | E21 Person          |          21 |
| Pozzo, Cassiano dal                    | E21 Person          |          19 |
| Crespi, Giuseppe Maria                 | E21 Person          |          18 |
| Guercino (Francesco Barbieri)          | E53 Place           |          17 |
| Medici, Grand Prince Ferdinand de'     | E21 Person          |          17 |
| Giordano, Luca                         | E21 Person          |          16 |
| Zanetti, A. M., the Elder              | E21 Person          |          16 |

## 4. 数据一致性检查

所有实体的类型分类一致 (没有发现同一实体被标记为不同类型的情况)。