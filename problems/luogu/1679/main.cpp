#include <bits/stdc++.h>
using namespace std;

const int MAXM = 100005;
const int INF = 1e9;

int m;
vector<int> pows;      // 所有不超过 m 的四次方数
vector<int> dp;        // dp[j] 表示凑出 j 的最少四次方数个数

void read_input() {
    cin >> m;
}

void solve() {
    for (int i = 1; ; i++) {
        long long x = 1LL * i * i * i * i;
        if (x > m) {
            break;
        }
        pows.push_back((int)x);
    }

    dp.assign(m + 1, INF);
    dp[0] = 0;

    for (int i = 0; i < (int)pows.size(); i++) {
        int w = pows[i];
        // 完全背包：同一种四次方数可以重复使用，所以容量正序枚举。
        for (int j = w; j <= m; j++) {
            if (dp[j - w] + 1 < dp[j]) {
                dp[j] = dp[j - w] + 1;
            }
        }
    }

    cout << dp[m] << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_input();
    solve();

    return 0;
}
