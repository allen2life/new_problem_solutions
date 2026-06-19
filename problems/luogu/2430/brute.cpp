#include <bits/stdc++.h>
using namespace std;

// brute.cpp：小数据暴力解，用来帮助理解题意并辅助对拍。

const int MAXN = 105;
const int MAXM = 105;

int wky_skill, wang_skill;
int m, n, limit_time;
int topic_time[MAXN]; // 老王做知识点 i 的题需要的时间
int cost[MAXM];       // WKY 做第 i 道题需要的时间
int reward_value[MAXM];
int answer;

// 枚举每道题“做 / 不做”两种选择。
// 这个做法复杂度是 O(2^m)，只适合小数据验证。
void dfs(int idx, int used_time, int total_reward) {
    if (used_time > limit_time) {
        return;
    }
    if (idx > m) {
        answer = max(answer, total_reward);
        return;
    }

    dfs(idx + 1, used_time, total_reward);
    dfs(idx + 1, used_time + cost[idx], total_reward + reward_value[idx]);
}

void read_input() {
    cin >> wky_skill >> wang_skill;
    cin >> m >> n;
    for (int i = 1; i <= n; i++) {
        cin >> topic_time[i];
    }

    int ratio = wang_skill / wky_skill;
    for (int i = 1; i <= m; i++) {
        int p, q;
        cin >> p >> q;
        cost[i] = topic_time[p] * ratio;
        reward_value[i] = q;
    }
    cin >> limit_time;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_input();
    dfs(1, 0, 0);
    cout << answer << '\n';

    return 0;
}
