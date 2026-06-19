// brute.cpp：小数据暴力解，用来帮助理解题意并辅助对拍。
#include <bits/stdc++.h>
using namespace std;

const int MAXM = 1005;

int total_time;         // 总可用时间
int herb_count;         // 草药数量
int need_time[MAXM];    // 每株草药需要的时间
int herb_value[MAXM];   // 每株草药的价值
int best_answer;        // 当前找到的最大总价值

void dfs(int idx, int used_time, int total_value) {
    if (used_time > total_time) {
        return;
    }
    if (idx > herb_count) {
        best_answer = max(best_answer, total_value);
        return;
    }

    // 选择第 idx 株草药。
    dfs(idx + 1, used_time + need_time[idx], total_value + herb_value[idx]);
    // 不选择第 idx 株草药。
    dfs(idx + 1, used_time, total_value);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> total_time >> herb_count;
    for (int i = 1; i <= herb_count; i++) {
        cin >> need_time[i] >> herb_value[i];
    }

    best_answer = 0;
    dfs(1, 0, 0);

    cout << best_answer << '\n';
    return 0;
}
