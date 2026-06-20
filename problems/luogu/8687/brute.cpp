#include <bits/stdc++.h>
using namespace std;

int n, m, k;
int pack_mask[105];
int full_mask;
int ans;

void dfs_choose(int idx, int mask, int used) {
    if (used >= ans) {
        return;
    }
    if (mask == full_mask) {
        ans = min(ans, used);
        return;
    }
    if (idx == n + 1) {
        return;
    }

    dfs_choose(idx + 1, mask, used);
    dfs_choose(idx + 1, mask | pack_mask[idx], used + 1);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // brute.cpp：枚举买哪些包糖果，统计能否覆盖所有口味。
    cin >> n >> m >> k;
    for (int i = 1; i <= n; i++) {
        int mask = 0;
        for (int j = 1; j <= k; j++) {
            int x;
            cin >> x;
            mask |= 1 << (x - 1);
        }
        pack_mask[i] = mask;
    }

    full_mask = (1 << m) - 1;
    ans = n + 1;
    dfs_choose(1, 0, 0);

    if (ans == n + 1) {
        cout << -1 << '\n';
    } else {
        cout << ans << '\n';
    }
    return 0;
}
