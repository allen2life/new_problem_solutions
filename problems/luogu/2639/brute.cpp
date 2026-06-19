#include <bits/stdc++.h>
using namespace std;

// brute.cpp：小数据暴力解，用来帮助理解题意并辅助对拍。

const int MAXN = 505;

int h, n;
int weight[MAXN];
int answer;

// 枚举每捆干草吃或不吃。
// 复杂度 O(2^n)，只适合小数据验证。
void dfs(int idx, int total_weight) {
    if (total_weight > h) {
        return;
    }
    if (idx > n) {
        answer = max(answer, total_weight);
        return;
    }

    dfs(idx + 1, total_weight);
    dfs(idx + 1, total_weight + weight[idx]);
}

void read_input() {
    cin >> h >> n;
    for (int i = 1; i <= n; i++) {
        cin >> weight[i];
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_input();
    dfs(1, 0);
    cout << answer << '\n';

    return 0;
}
