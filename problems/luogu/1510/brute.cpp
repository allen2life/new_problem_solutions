// brute.cpp：小数据暴力解，用来帮助理解题意并辅助对拍。
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 10005;

int need_volume;          // 至少需要填平的体积
int n;                    // 木石数量
int stamina_limit;        // 剩余体力
int volume_gain[MAXN];    // 木石体积
int stamina_cost[MAXN];   // 木石体力消耗
int best_cost;            // 达到目标体积时的最小体力消耗

void dfs(int idx, int sum_volume, int sum_cost) {
    if (sum_cost >= best_cost) {
        return;
    }
    if (sum_volume >= need_volume) {
        best_cost = min(best_cost, sum_cost);
        return;
    }
    if (idx > n) {
        return;
    }

    // 选择第 idx 块木石。
    dfs(idx + 1, sum_volume + volume_gain[idx], sum_cost + stamina_cost[idx]);
    // 不选择第 idx 块木石。
    dfs(idx + 1, sum_volume, sum_cost);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> need_volume >> n >> stamina_limit;
    for (int i = 1; i <= n; i++) {
        cin >> volume_gain[i] >> stamina_cost[i];
    }

    best_cost = 0x3f3f3f3f;
    dfs(1, 0, 0);

    if (best_cost > stamina_limit) {
        cout << "Impossible\n";
    } else {
        cout << stamina_limit - best_cost << '\n';
    }

    return 0;
}
