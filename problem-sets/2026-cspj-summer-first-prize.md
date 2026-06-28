---
title: "2026 CSP-J 暑期一等奖训练题单"
description: "根据 2026 CSP-J 暑期一等奖训练计划整理的阶段训练题单。"
---

# 2026 CSP-J 暑期一等奖训练题单

本题单根据根目录下的 `2026-cspj-暑期一等奖训练计划.md` 整理，目标是服务 8 周暑期训练。

这不是普通刷题清单。每一道核心题都要完成下面的训练闭环：

```text
暴力解 -> 复杂度瓶颈 -> 优化方向 -> 正确性证明 -> 正解代码 -> 对拍/复盘
```

每题完成后必须写清楚四件事：

```text
暴力怎么写：
瓶颈在哪里：
正解消掉了哪一层复杂度：
下次看到什么特征要想到这个方法：
```

训练目标：

```text
T1：100 分，必须稳定
T2：90-100 分，基本零失误
T3：70-100 分，重点突破
T4：30-60 分，稳定拿部分分
总分目标：290-330+
```

## 第 1-2 周：DP 基础转化

目标：把“我只能写暴力”变成“我知道暴力哪里慢，并能尝试设计状态”。

- [ ] [[problem: luogu,P1002]]
- [ ] [[problem: luogu,P1216]]
- [ ] [[problem: luogu,P1115]]
- [ ] [[problem: luogu,P1057]]
- [ ] [[problem: luogu,P1970]]
- [ ] [[problem: luogu,P3399]]
- [ ] [[problem: luogu,P1103]]
- [ ] [[problem: luogu,P7074]]
- [ ] [[problem: luogu,P8816]]
- [ ] [[problem: luogu,P1507]]
- [ ] [[problem: luogu,P1048]]
- [ ] [[problem: luogu,P1049]]
- [ ] [[problem: luogu,P1164]]
- [ ] [[problem: luogu,P2347]]
- [ ] [[problem: luogu,P1877]]

过关标准：

```text
能先写出暴力搜索或枚举。
能指出暴力中的重复子问题。
能定义 dp 数组的含义。
能写出转移方程并解释每一项来自哪里。
```

## 第 3-4 周：数学、贪心与规律专项

目标：解决“能写暴力，但不知道怎么优化”和“想到贪心但不会证明”。

- [ ] [[problem: luogu,P9749]]
- [ ] [[problem: luogu,P9750]]
- [ ] [[problem: luogu,P8814]]
- [ ] [[problem: luogu,P7909]]
- [ ] [[problem: luogu,P9748]]
- [ ] [[problem: luogu,P8177]]
- [ ] [[problem: luogu,P6625]]
- [ ] [[problem: luogu,P1824]]
- [ ] [[problem: luogu,P2920]]
- [ ] [[problem: luogu,P2985]]
- [ ] [[problem: luogu,P2678]]
- [ ] [[problem: luogu,P1969]]
- [ ] [[problem: luogu,P3585]]
- [ ] [[problem: luogu,P9974]]
- [ ] [[problem: luogu,P3817]]
- [ ] [[problem: luogu,P3392]]
- [ ] [[problem: luogu,P1109]]
- [ ] [[problem: luogu,P2239]]
- [ ] [[problem: luogu,P1887]]
- [ ] [[problem: luogu,P9585]]

过关标准：

```text
能解释为什么排序有用。
能解释为什么局部选择不会影响全局最优。
能从 O(n^2) 或 O(n^3) 暴力中看出可以预处理、前缀、排序或二分。
能把证明写成 3-5 句话，而不是只说“感觉是这样”。
```

## 第 5-6 周：近三年 CSP-J 真题锚点

目标：对准近三年 CSP-J T3/T4 的真实风格，训练考试转化能力。

这些题必须做两遍：

```text
第一遍：限时完成，记录真实得分。
第二遍：复盘后重写，补齐暴力分、特殊性质分和正解。
```

### 2023 CSP-J

- [ ] [[problem: luogu,P9748]]
- [ ] [[problem: luogu,P9749]]
- [ ] [[problem: luogu,P9750]]
- [ ] [[problem: luogu,P9751]]

### 2024 CSP-J

- [ ] [[problem: luogu,P11227]]
- [ ] [[problem: luogu,P11228]]
- [ ] [[problem: luogu,P11229]]
- [ ] [[problem: luogu,P11230]]

### 2025 CSP-J

- [ ] [[problem: luogu,P14357]]
- [ ] [[problem: luogu,P14358]]
- [ ] [[problem: luogu,P14359]]
- [ ] [[problem: luogu,P14360]]

过关标准：

```text
T3 能稳定写出暴力和部分优化。
T3 能在复盘后独立写出正解。
T4 能先拿暴力分，不空题。
T4 能识别特殊性质，并写出对应部分分代码。
```

## 第 5-6 周：综合实现与考试转化

目标：解决“思路知道，但代码写不稳、调不出、考场拿不到分”的问题。

- [ ] [[problem: luogu,P7910]]
- [ ] [[problem: luogu,P7911]]
- [ ] [[problem: luogu,P8815]]
- [ ] [[problem: luogu,P7073]]
- [ ] [[problem: luogu,P7912]]
- [ ] [[problem: luogu,P1175]]
- [ ] [[problem: luogu,P2058]]
- [ ] [[problem: luogu,P1886]]
- [ ] [[problem: luogu,P3662]]
- [ ] [[problem: luogu,P5542]]
- [ ] [[problem: luogu,P1147]]
- [ ] [[problem: luogu,P2895]]
- [ ] [[problem: luogu,P5663]]
- [ ] [[problem: luogu,P9751]]
- [ ] [[problem: luogu,P1330]]

过关标准：

```text
能在限时内写出可运行代码。
能处理边界和特殊数据。
能通过样例、自造数据和必要的对拍。
不会因为一个实现细节卡死整道题。
```

## 第 7-8 周：模拟赛与稳分策略

最后两周不再大规模扩题，重点训练考试分数转化。

每周安排：

```text
2 次完整模拟赛
2 次错题重写
1 次 T3/T4 专项
1 次 T1/T2 零失误训练
1 天轻量复盘
```

每次模拟赛后必须完成：

```text
1. 统计每题实际得分。
2. 标记失分原因：不会想、想到了但不会证、会想但写错、时间不够、低级错误。
3. T1/T2 的错误必须当天重写。
4. T3/T4 至少补出暴力和正解思路。
5. 第二天重写最关键的 1-2 道题。
```

考试时间分配建议：

```text
0-40 分钟：T1 完成并检查
40-100 分钟：T2 完成并检查
100-190 分钟：主攻 T3
190-240 分钟：T4 暴力分 + 特殊性质
最后 30 分钟：回查 T1/T2/T3
```

## 追加训练：DP 深化题

下面这些题来自原训练计划的 72 题核心清单。若前 6 周进度稳定，可以作为 DP 深化训练；若模拟赛暴露 DP 转化问题，也从这里回补。

- [ ] [[problem: luogu,P1388]]
- [ ] [[problem: luogu,P1977]]
- [ ] [[problem: luogu,P2800]]
- [ ] [[problem: luogu,P3009]]
- [ ] [[problem: luogu,P7158]]
- [ ] [[problem: luogu,P1855]]
- [ ] [[problem: luogu,P1616]]
- [ ] [[problem: luogu,P1832]]
- [ ] [[problem: luogu,P1077]]
- [ ] [[problem: luogu,P5662]]

## 最终执行原则

1. 每天宁可少做题，也要完成“暴力到正解”的完整链路。
2. T1/T2 错误必须当天清零，不能积压。
3. T3 是一等奖核心突破点，复盘质量比题量更重要。
4. T4 不追求每题正解，但必须训练稳定拿部分分。
5. 每周模拟赛的分数趋势比单题 AC 数更重要。
