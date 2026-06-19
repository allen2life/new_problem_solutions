#include <bits/stdc++.h>
using namespace std;

// brute.cpp：枚举每个食品选或不选，直接检查总体积和总质量是否合法。

int H, T, n;
int h[55], t[55], k[55];
int ans;

void dfs(int idx, int vh, int vt, int cal) {
    if (vh > H || vt > T) {
        return;
    }
    if (idx > n) {
        ans = max(ans, cal);
        return;
    }

    dfs(idx + 1, vh, vt, cal);
    dfs(idx + 1, vh + h[idx], vt + t[idx], cal + k[idx]);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> H >> T;
    cin >> n;

    for (int i = 1; i <= n; i++) {
        cin >> h[i] >> t[i] >> k[i];
    }

    ans = 0;
    dfs(1, 0, 0, 0);

    cout << ans << '\n';
    return 0;
}
