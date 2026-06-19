#include <bits/stdc++.h>
using namespace std;

// brute.cpp：递归枚举最后一次乘法拆分位置和左右乘号数量。

const int MAXN = 20;

int n, k;
int a[MAXN];
int sum[MAXN];

int range_sum(int l, int r) {
    return sum[r] - sum[l - 1];
}

int solve(int l, int r, int t) {
    if (t == 0) {
        return range_sum(l, r);
    }

    int best = 0;

    for (int mid = l; mid < r; mid++) {
        int left_len = mid - l + 1;
        int right_len = r - mid;

        for (int x = 0; x <= t - 1; x++) {
            if (x >= left_len || t - 1 - x >= right_len) {
                continue;
            }
            best = max(best, solve(l, mid, x) * solve(mid + 1, r, t - 1 - x));
        }
    }

    return best;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> k;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        sum[i] = sum[i - 1] + a[i];
    }

    cout << solve(1, n, k) << '\n';
    return 0;
}
