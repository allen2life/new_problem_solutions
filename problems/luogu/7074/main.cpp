#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1005;
const long long NEG_INF = -(1LL << 60);

int n, m;
int a[MAXN][MAXN];
long long dp[MAXN];   // 上一列结束在第 i 行的最大和
long long down[MAXN]; // 当前列内从上往下扫
long long up[MAXN];   // 当前列内从下往上扫

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            cin >> a[i][j];
        }
    }

    for (int i = 1; i <= n; i++) {
        dp[i] = NEG_INF;
    }
    dp[1] = 0;

    for (int j = 1; j <= m; j++) {
        down[1] = dp[1] + a[1][j];
        for (int i = 2; i <= n; i++) {
            // 要么这一列从左边直接进到第 i 行，
            // 要么已经在这一列走到第 i-1 行，再继续向下走。
            down[i] = max(dp[i], down[i - 1]) + a[i][j];
        }

        up[n] = dp[n] + a[n][j];
        for (int i = n - 1; i >= 1; i--) {
            // 对称地计算“从下往上走”这一类状态。
            up[i] = max(dp[i], up[i + 1]) + a[i][j];
        }

        for (int i = 1; i <= n; i++) {
            dp[i] = max(down[i], up[i]);
        }
    }

    cout << dp[n] << '\n';
    return 0;
}
