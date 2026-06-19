#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100000 + 5;
int school[MAXN], stu[MAXN];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m, n;
    cin >> m >> n;

    for (int i = 1; i <= m; i++) cin >> school[i];
    for (int i = 1; i <= n; i++) cin >> stu[i];

    sort(school + 1, school + m + 1);

    long long ans = 0;
    for (int i = 1; i <= n; i++) {
        int x = stu[i];
        int pos = lower_bound(school + 1, school + m + 1, x) - school;

        int best = 2000000000;
        if (pos <= m) best = min(best, abs(school[pos] - x));
        if (pos > 1) best = min(best, abs(school[pos - 1] - x));
        ans += best;
    }

    cout << ans << '\n';
    return 0;
}
