#include <bits/stdc++.h>
using namespace std;

// brute.cpp：暴力枚举最后一组的右端点，搜索所有合法分组方案。

const int MAXN = 35;
const int NEG_INF = -1000000000;

int n;
long long a[MAXN];
long long pre[MAXN];

// dfs(pos) 表示从第 pos 头牛开始分组，最多还能分出多少组。
int dfs(int pos) {
    if (pos > n) {
        return 0;
    }

    int best = NEG_INF;

    for (int r = pos; r <= n; r++) {
        long long seg_sum = pre[r] - pre[pos - 1];
        if (seg_sum >= 0) {
            best = max(best, 1 + dfs(r + 1));
        }
    }

    return best;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        pre[i] = pre[i - 1] + a[i];
    }

    cout << max(0, dfs(1)) << '\n';
    return 0;
}
