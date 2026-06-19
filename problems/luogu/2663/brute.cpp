// brute.cpp：小数据暴力解，用来帮助理解题意并辅助对拍。
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;

int n;               // 学生人数
int need_cnt;        // 必须选出的人数
int limit_score;     // 选出队伍的总分上限
int a[MAXN];         // 每个学生的分数
int best_answer;     // 当前找到的最优答案

void dfs(int idx, int picked, int sum_score) {
    if (sum_score > limit_score) {
        return;
    }
    if (picked > need_cnt) {
        return;
    }
    if (picked + (n - idx + 1) < need_cnt) {
        return;
    }
    if (best_answer == limit_score) {
        return;
    }

    if (idx > n) {
        if (picked == need_cnt) {
            best_answer = max(best_answer, sum_score);
        }
        return;
    }

    // 选第 idx 个学生。
    dfs(idx + 1, picked + 1, sum_score + a[idx]);
    // 不选第 idx 个学生。
    dfs(idx + 1, picked, sum_score);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    need_cnt = n / 2;

    int total_score = 0;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        total_score += a[i];
    }

    limit_score = total_score / 2;
    best_answer = 0;
    dfs(1, 0, 0);

    cout << best_answer << '\n';
    return 0;
}
