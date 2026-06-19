// brute.cpp：小数据暴力解，用来帮助理解题意并辅助对拍。
#include <bits/stdc++.h>
using namespace std;

const int MAXM = 1005;

int budget;             // 总预算
int item_count;         // 物品数量
int price[MAXM];        // 价格
int importance[MAXM];   // 重要度
int best_answer;        // 当前最大满意度

void dfs(int idx, int used_money, int total_value) {
    if (used_money > budget) {
        return;
    }
    if (idx > item_count) {
        best_answer = max(best_answer, total_value);
        return;
    }

    // 选择第 idx 个物品。
    dfs(idx + 1,
        used_money + price[idx],
        total_value + price[idx] * importance[idx]);

    // 不选择第 idx 个物品。
    dfs(idx + 1, used_money, total_value);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> budget >> item_count;
    for (int i = 1; i <= item_count; i++) {
        cin >> price[i] >> importance[i];
    }

    best_answer = 0;
    dfs(1, 0, 0);

    cout << best_answer << '\n';
    return 0;
}
