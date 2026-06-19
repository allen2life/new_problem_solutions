#include <bits/stdc++.h>
using namespace std;

static int N;
static long long M;
static vector<int> K, C;
static int limit;
static vector<long long> best;

static long long clamp_mul(long long a, int b) {
    __int128 v = (__int128)a * b;
    if (v > M) {
        return M;
    }
    return (long long)v;
}

static void dfs(int idx, int cost, long long ways) {
    if (cost > limit) {
        return;
    }
    if (idx == N) {
        best[cost] = max(best[cost], ways);
        return;
    }

    // 不买这个英雄的皮肤。
    dfs(idx + 1, cost, ways);

    // 枚举买 2..K[i] 款皮肤的情况。
    for (int x = 2; x <= K[idx]; ++x) {
        int nc = cost + x * C[idx];
        if (nc > limit) {
            break;
        }
        dfs(idx + 1, nc, clamp_mul(ways, x));
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> N >> M;
    K.resize(N);
    C.resize(N);
    for (int i = 0; i < N; ++i) {
        cin >> K[i];
    }
    for (int i = 0; i < N; ++i) {
        cin >> C[i];
    }

    limit = 0;
    for (int i = 0; i < N; ++i) {
        limit += K[i] * C[i];
    }

    best.assign(limit + 1, 0);
    dfs(0, 0, 1);

    for (int cost = 0; cost <= limit; ++cost) {
        if (best[cost] >= M) {
            cout << cost << '\n';
            return 0;
        }
    }

    return 0;
}
