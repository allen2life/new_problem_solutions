#include <bits/stdc++.h>
using namespace std;

const int MAXS = 1005;

int s;                  // 总和上限
int divisor_sum[MAXS];  // divisor_sum[i] = i 的真约数和
int dp[MAXS];           // dp[j] = 和不超过 j 时的最大约数和

void read_input() {
    cin >> s;
}

void build_divisor_sum() {
    memset(divisor_sum, 0, sizeof(divisor_sum));
    for (int d = 1; d <= s / 2; d++) {
        for (int multiple = d + d; multiple <= s; multiple += d) {
            divisor_sum[multiple] += d;
        }
    }
}

void solve() {
    build_divisor_sum();
    memset(dp, 0, sizeof(dp));

    for (int x = 1; x <= s; x++) {
        // 每个正整数只能选一次，所以按 0/1 背包倒序枚举。
        for (int j = s; j >= x; j--) {
            dp[j] = max(dp[j], dp[j - x] + divisor_sum[x]);
        }
    }

    cout << dp[s] << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_input();
    solve();

    return 0;
}
