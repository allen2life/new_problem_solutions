# 题目关系 pre/common 补全 - 工作记录

**日期**: 2026-06-07

**校验结果**: `python3 scripts/problem-analysis-tools/check_relations.py --all`
```
检查题目数：172
通过：关系字段符合当前规范。
```

---

## 概述

按照 `todo_problem_relations.md` 的计划，完成了 P0 到 P2 共 6 个批次的 pre/common 关系补全。

累计修改 **53 个文件**（含跳过已完成的 P2515）。

---

## P0：割点 / 双连通分量（7 题）

| 题目 | 写入 `pre` | 写入 `common` |
|------|-----------|--------------|
| POJ 1144 Network | — | POJ 1523（同为基础割点模板） |
| POJ 1523 SPF | POJ 1144（更基础的割点模板） | POJ 1144 |
| luogu P5058 嗅探器 | POJ 1144（基本 Tarjan 割点框架） | — |
| luogu P3225 矿场搭建 | POJ 1523（v-BCC 分解概念） | HDU 3394（同为 v-BCC 计数分类） |
| POJ 2942 Knights of the Round Table | POJ 1523（v-BCC + 边入栈写法） | — |
| OpenJ_Bailian 3091 Road Construction | POJ 1144（Tarjan DFS 框架） | — |
| HDU 3394 Railway | POJ 1523（v-BCC 分解） | luogu P3225（同为 v-BCC 计数分类） |

### 未写入候选及原因

- **POJ 2942 缺少二分图染色前置**：仓库中没有专门的二分图染色模板题，无法添加该方向 pre。候选记录：二分图染色基础题。
- **OpenJ_Bailian 3091（边双）未与 v-BCC 题互写 common**：边双与点双虽然是 Tarjan 体系，但概念和判定条件不同，强行 common 会误导。

---

## P1：欧拉路 / 欧拉回路（9 题）

| 题目 | 写入 `pre` | 写入 `common` |
|------|-----------|--------------|
| HDU 1878 欧拉回路 | — | OpenJ_Bailian 1300（同为无向图欧拉判定） |
| HDU 1116 Play on Words | HDU 1878（无向→有向度数条件） | luogu P1127（同为有向图欧拉建模） |
| HDU 5883 The Best Path | HDU 1878（度数条件+异或计算） | — |
| OpenJ_Bailian 1041 John's trip | HDU 1878（判定→Hierholzer 构造） | luogu P1341（同为 Hierholzer 字典序最小） |
| OpenJ_Bailian 1300 Door Man | HDU 1878（基本条件→带起终点） | HDU 1878 |
| OpenJ_Bailian 1392 Ouroboros Snake | HDU 1878（De Bruijn 建模基础） | — |
| OpenJ_Bailian 2513 Colored Sticks | HDU 1878（基本判定，同 P1333） | — |
| luogu P1127 词链 | HDU 1116（有向判定→构造输出） | HDU 1116 |
| luogu P1341 无序字母对 | HDU 1878（判定→Hierholzer） | OpenJ_Bailian 1041（同为 Hierholzer） |

### 未写入候选及原因

- **OpenJ_Bailian 1392（De Bruijn）的 common 未写**：De Bruijn 序列建模非常特殊，与标准欧拉路题不在同一个训练层级，不适合简单 common。

---

## P1：二分 / 二分答案（8 题）

| 题目 | 写入 `pre` | 写入 `common` |
|------|-----------|--------------|
| POJ 3122 Pie | — | luogu P1873（同为二分答案入门，实数 vs 整数） |
| POJ 2976 Dropping tests | luogu P1873（二分答案→分数规划变换） | luogu P3199（同为分数规划，验证手段不同） |
| OpenJ_Bailian 4135 Monthly Expense | luogu P1873（基本二分答案→分段验证） | luogu P1873 |
| atcoder abc248_d Range Count Query | — | luogu P1678（同为二分查找基本应用） |
| luogu P1678 烦恼的高考志愿 | — | atcoder abc248_d（同为二分查找基本应用） |
| luogu P1873 EKO / 砍树 | — | OpenJ_Bailian 4135（同为二分答案，check 不同） |
| luogu P1419 寻找段落 | luogu P1873（二分答案+单调队列组合） | — |
| luogu P3199 最小圈 | POJ 2976（分数规划→SPFA 判负环） | POJ 2976（同为分数规划） |

### 未写入候选及原因

- **POJ 2976 未与 POJ 3122 互写 common**：分数规划与普通二分在变换思想上差距较大，表面相似但训练目标不同。
- **luogu P1419 未与纯二分题 common**：它组合了单调队列技巧，属于交叉领域，不适合归入纯二分组。

---

## P1：网络流 / 费用流 / 最小割（14 题）

### 最大流子组

| 题目 | 写入 `pre` | 写入 `common` |
|------|-----------|--------------|
| HDU 3549 Flow Problem | —（最基础模板） | — |
| luogu P2763 试题库问题 | HDU 3549（最大流→二分图多重匹配） | — |
| luogu P2764 最小路径覆盖 | HDU 3549（最大流→拆点法） | luogu P2765（同为 DAG 最小路径覆盖） |
| luogu P2765 魔术球问题 | luogu P2764（静态→动态加点） | luogu P2764 |
| luogu P2766 最长不下降子序列 | HDU 3549（最大流→拆点限制） | — |

### 最小割子组

| 题目 | 写入 `pre` | 写入 `common` |
|------|-----------|--------------|
| luogu P2774 方格取数 | HDU 3549（最大流=最小割→黑白染色建模） | luogu P3749（同为 S-正权-T-负权 建图） |
| luogu P4001 狼抓兔子 | luogu P2774（基本最小割→对偶图技巧） | — |
| luogu P3749 寿司餐厅 | luogu P2774（最小割→最大权闭合子图） | — |

### 费用流子组

| 题目 | 写入 `pre` | 写入 `common` |
|------|-----------|--------------|
| luogu P4014 分配问题 | HDU 3549（最大流→MCMF） | luogu P4015（同为费用流供需匹配） |
| luogu P4015 运输问题 | luogu P4014（基本 MCMF→多源多汇） | luogu P4014 |
| luogu P4013 数字梯形 | luogu P4014（基本 MCMF→三级容量分层） | — |
| luogu P4016 负载平衡 | luogu P4014（基本 MCMF→环形均分纸牌） | — |
| luogu P2053 修车 | luogu P4014（基本 MCMF→调度维度拆点） | — |
| luogu P3358 K可重区间集 | luogu P4014（基本 MCMF→链式主干道） | — |

### 未写入候选及原因

- **最小割子组与费用流子组之间不加 common**：建模思路差异大，不应混淆。
- **luogu P4001（对偶图）未与普通最小割题 common**：对偶图技巧非常特殊，不具普适性。

---

## P2：单调队列 / 单调栈（6 题）

| 题目 | 写入 `pre` | 写入 `common` |
|------|-----------|--------------|
| luogu P2032 扫描 | — | luogu P1714（同为滑动窗口+单调队列） |
| luogu P1714 切蛋糕 | luogu P2032（基本单调队列→前缀和+窗口） | luogu P2032 |
| luogu P2627 Mowing the Lawn G | luogu P2032（基本单调队列→DP 优化） | — |
| luogu P2629 好消息，坏消息 | luogu P1714（前缀和+窗口→断环成链） | luogu P1714 |
| luogu P1198 [JSOI2008] 最大数 | luogu P2947（单调栈→多解法对比） | — |
| luogu P2947 Look Up S | —（基础单调栈模板） | — |

### 未写入候选及原因

- **P2627 未与 P2032 写 common**：DP 优化与滑动窗口模板差距较大。
- **P1198（todo）仅写入 pre**：文件本身标注 todo，内容不完整，不宜添加 common。

---

## P2：DP / 背包 / 树形 DP（9 题，1 题跳过）

| 题目 | 写入 `pre` | 写入 `common` |
|------|-----------|--------------|
| HDU 1003 Max Sum | — | POJ 3176（同为线性 DP 入门） |
| HDU 2602 Bone Collector | —（最基础背包模板） | — |
| POJ 3176 Cow Bowling | — | HDU 1003（同为线性 DP 入门） |
| OpenJ_Bailian 2506 Tiling | POJ 3176（线性递推→高精度） | — |
| OpenJ_Bailian 1651 Multiplication Puzzle | —（区间 DP 入门） | — |
| luogu P2014 选课 | HDU 2602（0/1 背包→分组背包树形 DP） | — |
| luogu P2515 软件安装 | **已从 SCC 批次完成，跳过** | — |
| luogu P1642 规划 | P2014（树形背包）+ POJ 2976（分数规划） | luogu P4322（同为分数规划+树形 DP） |
| luogu P4322 最佳团体 | luogu P1642（组合→sz 优化） | luogu P1642 |

### 未写入候选及原因

- **HDU 2602 未与任何题写 common**：作为 0/1 背包最基础模板，它本身是其他题的前置，不需要 common。
- **OpenJ_Bailian 1651（区间 DP）未与同批次题 common**：区间 DP 与线性/树形 DP 差异较大，不强行归组。
- **OpenJ_Bailian 2506 的高精度特性**：只加了线性 DP 前置，未按高精度方向关联，仓库中缺乏高精度基础题。

---

## 未写入的全局候选

整体按照 skill 规范，以下情况不写入 formal frontmatter：

1. **仅有相同 tag**（如多个"dp"标签题）：表面相似但模型不同不写 common。
2. **目标题不存在**（如 POJ 2942 的二分图染色前置）：不编造不存在的题目。
3. **低置信度/待确认关系**：没有记录到 candidates.md（仓库已 .gitignore 对应目录）。

---

## 校验

```bash
$ python3 scripts/problem-analysis-tools/check_relations.py --all
检查题目数：172
通过：关系字段符合当前规范。
```

---

## 后续建议

1. **切割点 / 双连通分量** 的 candidates.md 可以整理：POJ 2942 的二分图染色前置、边双 vs 点双的显式区分说明。
2. **费用流模板题定位**：当前以 luogu P4014 作为费用流入口前置，后续可评估是否需要更基础的费用流模板题。
3. **单调栈系列**：P1198 标注 todo，当前仅给出了 BIT 实现，单调栈部分待补充后可以评估是否增加 common。
4. **区间 DP 子组**：OpenJ_Bailian 1651 是唯一区间 DP 题，后续如有更多区间 DP 题可补上组内 common。
