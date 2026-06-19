// brute.cpp：小数据暴力解，用来帮助理解题意并辅助对拍。
#include <bits/stdc++.h>
using namespace std;

const int MAXS = 1005;

int s;                  // 总和上限
int divisor_sum[MAXS];  // 真约数和
int best_answer;        // 当前最大约数和

void build_divisor_sum() {
    memset(divisor_sum, 0, sizeof(divisor_sum));
    for (int d = 1; d <= s / 2; d++) {
        for (int multiple = d + d; multiple <= s; multiple += d) {
            divisor_sum[multiple] += d;
        }
    }
}

void dfs(int current, int sum_value, int sum_weight) {
    if (sum_weight > s) {
        return;
    }
    if (current > s) {
        best_answer = max(best_answer, sum_value);
        return;
    }

    // 选择当前数字。
    dfs(current + 1,
        sum_value + divisor_sum[current],
        sum_weight + current);

    // 不选择当前数字。
    dfs(current + 1, sum_value, sum_weight);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> s;
    build_divisor_sum();

    best_answer = 0;
    dfs(1, 0, 0);

    cout << best_answer << '\n';
    return 0;
}
