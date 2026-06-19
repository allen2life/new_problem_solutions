#include <bits/stdc++.h>
using namespace std;

// brute.cpp：小数据暴力解，用来帮助理解题意并辅助对拍。

const int MAXN = 10005;

int t, n;
int cost[MAXN];
int points[MAXN];
int answer;

// 依次枚举每种题目可以选多少道。
// 复杂度很高，只适合小数据验证。
void dfs(int idx, int remain_time, int total_score) {
    if (idx > n) {
        answer = max(answer, total_score);
        return;
    }

    int limit = remain_time / cost[idx];
    for (int cnt = 0; cnt <= limit; cnt++) {
        dfs(idx + 1, remain_time - cnt * cost[idx], total_score + cnt * points[idx]);
    }
}

void read_input() {
    cin >> t >> n;
    for (int i = 1; i <= n; i++) {
        cin >> points[i] >> cost[i];
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_input();
    dfs(1, t, 0);
    cout << answer << '\n';

    return 0;
}
