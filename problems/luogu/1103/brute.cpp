#include <bits/stdc++.h>
using namespace std;

// brute.cpp：暴力枚举保留哪些书，然后计算不整齐度。

const int MAXN = 25;
const int INF = 1000000000;

struct Book {
    int h, w;
};

int n, k;
Book a[MAXN];
int keep_cnt;
int chosen[MAXN];
int ans;

bool cmp_book(const Book &lhs, const Book &rhs) {
    return lhs.h < rhs.h;
}

void dfs(int pos, int picked) {
    if (picked == keep_cnt) {
        int sum = 0;
        for (int i = 2; i <= keep_cnt; i++) {
            sum += abs(a[chosen[i]].w - a[chosen[i - 1]].w);
        }
        ans = min(ans, sum);
        return;
    }

    if (pos > n) {
        return;
    }

    if (n - pos + 1 < keep_cnt - picked) {
        return;
    }

    chosen[picked + 1] = pos;
    dfs(pos + 1, picked + 1);
    dfs(pos + 1, picked);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> k;
    for (int i = 1; i <= n; i++) {
        cin >> a[i].h >> a[i].w;
    }

    sort(a + 1, a + n + 1, cmp_book);

    keep_cnt = n - k;
    ans = INF;
    dfs(1, 0);

    cout << ans << '\n';
    return 0;
}
