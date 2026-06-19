#include <bits/stdc++.h>
using namespace std;

// brute.cpp：小数据暴力解，用来帮助理解题意并辅助对拍。

const int MAXN = 10005;

int t, m;
int cost[MAXN];
int value[MAXN];
long long answer;

// 依次枚举每种草药可以取多少次。
// 复杂度很高，只适合小数据验证。
void dfs(int idx, int remain_time, long long total_value) {
    if (idx > m) {
        answer = max(answer, total_value);
        return;
    }

    int limit = remain_time / cost[idx];
    for (int cnt = 0; cnt <= limit; cnt++) {
        dfs(idx + 1, remain_time - cnt * cost[idx], total_value + 1LL * cnt * value[idx]);
    }
}

void read_input() {
    cin >> t >> m;
    for (int i = 1; i <= m; i++) {
        cin >> cost[i] >> value[i];
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
