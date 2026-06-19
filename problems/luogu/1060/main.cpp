#include <bits/stdc++.h>
using namespace std;

const int MAXM = 1005;

int budget;             // 总预算
int item_count;         // 物品数量
int price[MAXM];        // 第 i 个物品的价格
int importance[MAXM];   // 第 i 个物品的重要度
vector<int> dp;         // dp[j] = 花费不超过 j 时能获得的最大满意度

void read_input() {
    cin >> budget >> item_count;
    for (int i = 1; i <= item_count; i++) {
        cin >> price[i] >> importance[i];
    }
}

void solve() {
    dp.assign(budget + 1, 0);

    for (int i = 1; i <= item_count; i++) {
        int value = price[i] * importance[i];
        // 倒序枚举预算，保证每个物品最多只买一次。
        for (int j = budget; j >= price[i]; j--) {
            dp[j] = max(dp[j], dp[j - price[i]] + value);
        }
    }

    cout << dp[budget] << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_input();
    solve();

    return 0;
}
