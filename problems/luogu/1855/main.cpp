#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;
const int MAXM = 205;
const int MAXT = 205;

int n;                      // 愿望数量
int limit_money, limit_time; // 可用的金钱和时间上限
int cost_money[MAXN];       // 第 i 个愿望需要的金钱
int cost_time[MAXN];        // 第 i 个愿望需要的时间
int dp[MAXM][MAXT];         // dp[j][k] = 金钱不超过 j、时间不超过 k 时最多能满足多少个愿望

void read_input() {
    cin >> n >> limit_money >> limit_time;
    for (int i = 1; i <= n; i++) {
        cin >> cost_money[i] >> cost_time[i];
    }
}

void solve() {
    memset(dp, 0, sizeof(dp));

    for (int i = 1; i <= n; i++) {
        // 两维容量都倒序，保证每个愿望最多只被选择一次。
        for (int j = limit_money; j >= cost_money[i]; j--) {
            for (int k = limit_time; k >= cost_time[i]; k--) {
                dp[j][k] = max(dp[j][k], dp[j - cost_money[i]][k - cost_time[i]] + 1);
            }
        }
    }

    cout << dp[limit_money][limit_time] << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_input();
    solve();

    return 0;
}
