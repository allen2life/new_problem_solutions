#include <bits/stdc++.h>
using namespace std;

const int TYPE_CNT = 6;
const int weight_value[TYPE_CNT + 1] = {0, 1, 2, 3, 5, 10, 20};
const int MAXW = 1005;

int cnt[TYPE_CNT + 1];  // 每种砝码的数量
bool dp[MAXW];          // dp[w] = 是否能恰好称出重量 w
int total_weight;       // 所有砝码总重量

void read_input() {
    total_weight = 0;
    for (int i = 1; i <= TYPE_CNT; i++) {
        cin >> cnt[i];
        total_weight += cnt[i] * weight_value[i];
    }
}

void solve() {
    memset(dp, 0, sizeof(dp));
    dp[0] = true;

    for (int i = 1; i <= TYPE_CNT; i++) {
        for (int c = 1; c <= cnt[i]; c++) {
            int w = weight_value[i];
            // 把每个砝码当成一件 0/1 物品。
            for (int sum = total_weight; sum >= w; sum--) {
                if (dp[sum - w]) {
                    dp[sum] = true;
                }
            }
        }
    }

    int answer = 0;
    for (int w = 1; w <= total_weight; w++) {
        if (dp[w]) {
            answer++;
        }
    }

    cout << "Total=" << answer << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_input();
    solve();

    return 0;
}
