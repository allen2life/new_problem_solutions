#include <bits/stdc++.h>
using namespace std;

const int MOD = 998244353;
const int MAXV = 5000;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> cnt(MAXV + 1, 0);
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        cnt[x]++;
    }

    // 预计算 2 的幂次
    vector<int> pow2(n + 1);
    pow2[0] = 1;
    for (int i = 1; i <= n; i++) {
        pow2[i] = pow2[i - 1] * 2 % MOD;
    }

    vector<int> dp(MAXV + 1, 0);
    dp[0] = 1; // 空集

    long long ans = 0;
    int total_cnt = 0; // 已处理的木棍总数

    for (int v = 1; v <= MAXV; v++) {
        int c = cnt[v];
        if (c == 0) continue;

        // dp 中为所有长度 < v 的木棍的子集
        int total_small = pow2[total_cnt]; // 更小木棍的全部子集数

        // 前缀和：子集和 ≤ v 的方案数
        int pref = 0;
        for (int s = 0; s <= v && s <= MAXV; s++) {
            pref = (pref + dp[s]) % MOD;
        }
        int sum_gt_v = (total_small - pref + MOD) % MOD;

        // k = 1：选恰好 1 根长度为 v 的木棍
        ans = (ans + 1LL * c * sum_gt_v) % MOD;

        // k = 2：选恰好 2 根长度为 v 的木棍
        if (c >= 2) {
            long long C2 = 1LL * c * (c - 1) / 2 % MOD;
            int non_empty_small = (total_small - 1 + MOD) % MOD;
            ans = (ans + C2 * non_empty_small) % MOD;
        }

        // k >= 3：选至少 3 根长度为 v 的木棍
        if (c >= 3) {
            long long C2 = 1LL * c * (c - 1) / 2 % MOD;
            int ge3 = ((pow2[c] - 1 - c - C2) % MOD + MOD) % MOD;
            ans = (ans + 1LL * ge3 * total_small) % MOD;
        }

        // 将 cnt[v] 根长度为 v 的木棍加入 dp（多重背包）
        for (int k = 0; k < c; k++) {
            for (int s = MAXV; s >= v; s--) {
                dp[s] = (dp[s] + dp[s - v]) % MOD;
            }
        }
        total_cnt += c;
    }

    cout << ans % MOD << '\n';
    return 0;
}
