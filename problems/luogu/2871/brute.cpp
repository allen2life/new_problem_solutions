#include <bits/stdc++.h>
using namespace std;

// brute.cpp：小数据暴力解，用来帮助理解题意并辅助对拍。

const int MAXN = 3405;

int n, m;
int weight[MAXN];
int value[MAXN];
int answer;

// 枚举每个物品选或不选。
// 复杂度是 O(2^n)，只适合小数据验证。
void dfs(int idx, int used_weight, int total_value) {
    if (used_weight > m) {
        return;
    }
    if (idx > n) {
        answer = max(answer, total_value);
        return;
    }

    dfs(idx + 1, used_weight, total_value);
    dfs(idx + 1, used_weight + weight[idx], total_value + value[idx]);
}

void read_input() {
    cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        cin >> weight[i] >> value[i];
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_input();
    dfs(1, 0, 0);
    cout << answer << '\n';

    return 0;
}
