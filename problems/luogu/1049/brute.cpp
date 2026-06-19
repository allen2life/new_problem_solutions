// brute.cpp：小数据暴力解，用来帮助理解题意并辅助对拍。
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 35;

int capacity;          // 箱子容量
int n;                 // 物品数量
int a[MAXN];           // 每个物品的体积
int best_fill;         // 当前能装下的最大总体积

void dfs(int idx, int sum_volume) {
    if (sum_volume > capacity) {
        return;
    }
    if (idx > n) {
        best_fill = max(best_fill, sum_volume);
        return;
    }

    // 选择第 idx 个物品。
    dfs(idx + 1, sum_volume + a[idx]);
    // 不选择第 idx 个物品。
    dfs(idx + 1, sum_volume);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> capacity;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    best_fill = 0;
    dfs(1, 0);

    cout << capacity - best_fill << '\n';
    return 0;
}
