#include <bits/stdc++.h>
using namespace std;

const int MAXN = 10005;
const int MAXV = 10005;
const int INF = 0x3f3f3f3f;

int need_volume;          // 至少需要填平的体积
int n;                    // 木石数量
int stamina_limit;        // 剩余体力
int volume_gain[MAXN];    // 第 i 块木石的体积
int stamina_cost[MAXN];   // 第 i 块木石需要的体力
int dp[MAXV];             // dp[j] = 达到体积 j (j 被截断到 need_volume) 所需的最小体力

void read_input() {
    cin >> need_volume >> n >> stamina_limit;
    for (int i = 1; i <= n; i++) {
        cin >> volume_gain[i] >> stamina_cost[i];
    }
}

void solve() {
    memset(dp, 0x3f, sizeof(dp));
    dp[0] = 0;

    for (int i = 1; i <= n; i++) {
        for (int j = need_volume; j >= 0; j--) {
            if (dp[j] == INF) {
                continue;
            }
            int nxt = j + volume_gain[i];
            if (nxt > need_volume) {
                nxt = need_volume;
            }
            dp[nxt] = min(dp[nxt], dp[j] + stamina_cost[i]);
        }
    }

    if (dp[need_volume] > stamina_limit) {
        cout << "Impossible\n";
    } else {
        cout << stamina_limit - dp[need_volume] << '\n';
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_input();
    solve();

    return 0;
}
