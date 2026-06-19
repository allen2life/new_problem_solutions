#include <bits/stdc++.h>
using namespace std;

const int MAXN = 55;
const int MAXV = 1005;

int n, begin_level, max_level;
int change_value[MAXN];
bool dp[MAXN][MAXV]; // dp[i][v] 表示调完前 i 次后，音量 v 是否可达

void read_input() {
    cin >> n >> begin_level >> max_level;
    for (int i = 1; i <= n; i++) {
        cin >> change_value[i];
    }
}

void solve() {
    dp[0][begin_level] = true;

    for (int i = 1; i <= n; i++) {
        for (int v = 0; v <= max_level; v++) {
            if (!dp[i - 1][v]) {
                continue;
            }

            int up = v + change_value[i];
            int down = v - change_value[i];

            if (up <= max_level) {
                dp[i][up] = true;
            }
            if (down >= 0) {
                dp[i][down] = true;
            }
        }
    }

    for (int v = max_level; v >= 0; v--) {
        if (dp[n][v]) {
            cout << v << '\n';
            return;
        }
    }

    cout << -1 << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_input();
    solve();

    return 0;
}
