#include <bits/stdc++.h>
using namespace std;

// brute.cpp：每个木块三种选择：放左塔 / 放右塔 / 不用，直接枚举。

int n;
int h[25];
int ans;

void dfs(int idx, int left_sum, int right_sum) {
    if (idx > n) {
        if (left_sum == right_sum && left_sum > 0) {
            ans = max(ans, left_sum);
        }
        return;
    }

    dfs(idx + 1, left_sum, right_sum);
    dfs(idx + 1, left_sum + h[idx], right_sum);
    dfs(idx + 1, left_sum, right_sum + h[idx]);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    for (int i = 1; i <= n; i++) {
        cin >> h[i];
    }

    ans = 0;
    dfs(1, 0, 0);

    cout << ans << '\n';
    return 0;
}
