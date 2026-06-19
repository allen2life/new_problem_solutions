#include <bits/stdc++.h>
using namespace std;

const int MAXH = 5005;
const int MAXC = 50005;

int c, h;
int volume[MAXH];
int dp[MAXC]; // dp[j] 表示总体积不超过 j 时，最多能装下多少体积的草捆

void read_input() {
    cin >> c >> h;
    for (int i = 1; i <= h; i++) {
        cin >> volume[i];
    }
}

void solve() {
    for (int i = 1; i <= h; i++) {
        // 每捆草最多只能买一次，所以容量必须倒序枚举。
        for (int j = c; j >= volume[i]; j--) {
            dp[j] = max(dp[j], dp[j - volume[i]] + volume[i]);
        }
    }

    cout << dp[c] << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_input();
    solve();

    return 0;
}
