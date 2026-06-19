#include <bits/stdc++.h>
using namespace std;

const int MAXN = 200005;

int n;
int a[MAXN];
long long dp[MAXN]; // dp[i]：以 i 结尾的最大子段和

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    dp[1] = a[1];
    long long ans = dp[1];
    for (int i = 2; i <= n; i++) {
        dp[i] = max(1LL * a[i], dp[i - 1] + a[i]);
        ans = max(ans, dp[i]);
    }

    cout << ans << '\n';
    return 0;
}
