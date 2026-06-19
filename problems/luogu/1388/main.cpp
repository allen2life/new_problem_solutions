#include <bits/stdc++.h>
using namespace std;

const int MAXN = 20;

int n, k;
int a[MAXN];
int sum[MAXN];
int dp[MAXN][MAXN][MAXN];

int range_sum(int l, int r) {
    return sum[r] - sum[l - 1];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> k;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        sum[i] = sum[i - 1] + a[i];
    }

    // dp[l][r][t] 表示区间 [l,r] 内恰好放 t 个乘号时的最大值。
    for (int len = 1; len <= n; len++) {
        for (int l = 1; l + len - 1 <= n; l++) {
            int r = l + len - 1;

            // 不放乘号时，整个区间只能全部用加号连接。
            dp[l][r][0] = range_sum(l, r);

            for (int t = 1; t < len; t++) {
                int best = 0;

                // 最后一次乘法把区间拆成左右两部分。
                // 左边放 x 个乘号，右边放 t-1-x 个乘号。
                for (int mid = l; mid < r; mid++) {
                    int left_len = mid - l + 1;
                    int right_len = r - mid;

                    for (int x = 0; x <= t - 1; x++) {
                        if (x >= left_len || t - 1 - x >= right_len) {
                            continue;
                        }
                        best = max(best, dp[l][mid][x] * dp[mid + 1][r][t - 1 - x]);
                    }
                }

                dp[l][r][t] = best;
            }
        }
    }

    cout << dp[1][n][k] << '\n';
    return 0;
}
