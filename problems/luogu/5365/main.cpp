#include <bits/stdc++.h>
using namespace std;

static long long clamp_mul(long long a, int b, long long limit) {
    __int128 v = (__int128)a * b;
    if (v > limit) {
        return limit;
    }
    return (long long)v;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    long long M;
    cin >> N >> M;

    vector<int> K(N), C(N);
    for (int i = 0; i < N; ++i) {
        cin >> K[i];
    }
    for (int i = 0; i < N; ++i) {
        cin >> C[i];
    }

    int limit = 0;
    for (int i = 0; i < N; ++i) {
        limit += K[i] * C[i];
    }

    vector<long long> dp(limit + 1, 0), ndp(limit + 1, 0);
    dp[0] = 1;

    for (int i = 0; i < N; ++i) {
        // 先保留“不买当前英雄”的情况。
        ndp = dp;

        for (int cost = 0; cost <= limit; ++cost) {
            if (dp[cost] == 0) {
                continue;
            }

            for (int x = 2; x <= K[i]; ++x) {
                int nc = cost + x * C[i];
                if (nc > limit) {
                    break;
                }
                // 选 x 款皮肤后，展示方式数乘上 x。
                ndp[nc] = max(ndp[nc], clamp_mul(dp[cost], x, M));
            }
        }

        dp.swap(ndp);
    }

    for (int cost = 0; cost <= limit; ++cost) {
        if (dp[cost] >= M) {
            cout << cost << '\n';
            return 0;
        }
    }

    return 0;
}
