#include <bits/stdc++.h>
using namespace std;

const int MAXC = 405;

int H, T, n;
int h[55], t[55], k[55];
int dp[MAXC][MAXC]; // dp[j][l]：体积不超过 j、质量不超过 l 时的最大卡路里

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> H >> T;
    cin >> n;

    for (int i = 1; i <= n; i++) {
        cin >> h[i] >> t[i] >> k[i];
    }

    for (int i = 1; i <= n; i++) {
        for (int j = H; j >= h[i]; j--) {
            for (int l = T; l >= t[i]; l--) {
                dp[j][l] = max(dp[j][l], dp[j - h[i]][l - t[i]] + k[i]);
            }
        }
    }

    cout << dp[H][T] << '\n';
    return 0;
}
