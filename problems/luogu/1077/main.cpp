#include <bits/stdc++.h>
using namespace std;

const int MOD = 1000007;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    // prev[j]：已经处理完前 i-1 种花后，摆出 j 盆花的方案数
    vector<int> prev(m + 1, 0), cur(m + 1, 0);
    prev[0] = 1;

    for (int i = 1; i <= n; i++) {
        cur[0] = 1;
        for (int j = 1; j <= m; j++) {
            long long val = cur[j - 1] + prev[j];
            if (j - a[i] - 1 >= 0) {
                val -= prev[j - a[i] - 1];
            }
            val %= MOD;
            if (val < 0) val += MOD;
            cur[j] = static_cast<int>(val);
        }
        swap(prev, cur);
    }

    cout << prev[m] << '\n';

    return 0;
}
