// brute.cpp：小数据暴力解，用来帮助理解题意并辅助对拍。
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;

int n;                       // 愿望数量
int limit_money, limit_time; // 可用资源上限
int cost_money[MAXN];        // 每个愿望需要的金钱
int cost_time[MAXN];         // 每个愿望需要的时间
int best_answer;             // 当前找到的最优答案

void dfs(int idx, int used_money, int used_time, int chosen_cnt) {
    if (used_money > limit_money || used_time > limit_time) {
        return;
    }
    if (chosen_cnt + (n - idx + 1) <= best_answer) {
        return;
    }
    if (idx > n) {
        best_answer = max(best_answer, chosen_cnt);
        return;
    }

    // 选择第 idx 个愿望。
    dfs(idx + 1,
        used_money + cost_money[idx],
        used_time + cost_time[idx],
        chosen_cnt + 1);

    // 不选择第 idx 个愿望。
    dfs(idx + 1, used_money, used_time, chosen_cnt);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> limit_money >> limit_time;
    for (int i = 1; i <= n; i++) {
        cin >> cost_money[i] >> cost_time[i];
    }

    best_answer = 0;
    dfs(1, 0, 0, 0);

    cout << best_answer << '\n';
    return 0;
}
