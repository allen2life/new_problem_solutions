// brute.cpp：小数据暴力解，用来帮助理解题意并辅助对拍。
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;

int n;
int limit_detect;          // 总探查风险上限
int limit_money;           // 总工资上限
int info_value[MAXN];      // 资料量
int detect_cost[MAXN];     // 探查风险
int money_cost[MAXN];      // 工资
int best_answer;           // 当前找到的最大资料量

void dfs(int idx, int used_detect, int used_money, int total_info) {
    if (used_detect > limit_detect || used_money > limit_money) {
        return;
    }
    if (idx > n) {
        best_answer = max(best_answer, total_info);
        return;
    }

    // 选择第 idx 个间谍。
    dfs(idx + 1,
        used_detect + detect_cost[idx],
        used_money + money_cost[idx],
        total_info + info_value[idx]);

    // 不选择第 idx 个间谍。
    dfs(idx + 1, used_detect, used_money, total_info);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> limit_detect >> limit_money;
    for (int i = 1; i <= n; i++) {
        cin >> info_value[i] >> detect_cost[i] >> money_cost[i];
    }

    best_answer = 0;
    dfs(1, 0, 0, 0);

    cout << best_answer << '\n';
    return 0;
}
