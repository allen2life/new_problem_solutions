#include <bits/stdc++.h>
using namespace std;

const int MAXK = 1005;

int n, k, p;
int dp[MAXK];
int ndp[MAXK];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> k >> p;

    dp[0] = 1 % p;

    for (int i = 1; i <= n; i++) {
        int upper = min(i, k);
        for (int j = 0; j <= upper; j++) {
            ndp[j] = 0;
        }

        for (int j = 1; j <= upper; j++) {
            // 第 i 个苹果单独开一个新篮子，或者放进已有的 j 个篮子之一。
            long long ways = dp[j - 1];
            ways += 1LL * j * dp[j];
            ndp[j] = ways % p;
        }

        for (int j = 0; j <= upper; j++) {
            dp[j] = ndp[j];
        }
    }

    cout << dp[k] % p << '\n';
    return 0;
}
