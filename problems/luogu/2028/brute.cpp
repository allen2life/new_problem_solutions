#include <bits/stdc++.h>
using namespace std;

// brute.cpp：暴力枚举每个苹果放进哪个篮子，只适合很小的数据。

int n, k, p;
long long ans;

void dfs(int idx, int used) {
    if (idx > n) {
        if (used == k) {
            ans++;
        }
        return;
    }

    // 放进已经开好的某一个篮子。
    for (int i = 1; i <= used; i++) {
        dfs(idx + 1, used);
    }

    // 开一个新篮子给当前苹果。
    if (used < k) {
        dfs(idx + 1, used + 1);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> k >> p;

    ans = 0;
    dfs(1, 0);

    cout << ans % p << '\n';
    return 0;
}
