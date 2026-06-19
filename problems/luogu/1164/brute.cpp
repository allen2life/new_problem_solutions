// brute.cpp：小数据暴力解，用来帮助理解题意并辅助对拍。
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;

int n;              // 菜品种类数
int money;          // 需要恰好花掉的钱
int a[MAXN];        // 每种菜的价格
int answer_count;   // 当前方案数

void dfs(int idx, int sum_money) {
    if (sum_money > money) {
        return;
    }
    if (idx > n) {
        if (sum_money == money) {
            answer_count++;
        }
        return;
    }

    // 选择第 idx 种菜。
    dfs(idx + 1, sum_money + a[idx]);
    // 不选择第 idx 种菜。
    dfs(idx + 1, sum_money);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> money;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    answer_count = 0;
    dfs(1, 0);

    cout << answer_count << '\n';
    return 0;
}
