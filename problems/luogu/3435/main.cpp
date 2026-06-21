#include <bits/stdc++.h>
using namespace std;

int n;
string s;
vector<int> pi_arr;
vector<int> min_border;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    cin >> s;
    s = " " + s;

    pi_arr.assign(n + 1, 0);
    min_border.assign(n + 1, 0);

    long long ans = 0;

    // pi_arr[i] 表示前缀 s[1..i] 的最长真前后缀长度。
    for (int i = 2; i <= n; i++) {
        int j = pi_arr[i - 1];
        while (j > 0 && s[j + 1] != s[i]) {
            j = pi_arr[j];
        }
        if (s[j + 1] == s[i]) {
            j++;
        }
        pi_arr[i] = j;

        // 所有 border 都在 pi 链上，最短非空 border 就是这条链的最后一个非零点。
        if (pi_arr[i] == 0) {
            min_border[i] = 0;
        }
        else if (min_border[pi_arr[i]] != 0) {
            min_border[i] = min_border[pi_arr[i]];
        }
        else {
            min_border[i] = pi_arr[i];
        }

        if (min_border[i] != 0) {
            ans += i - min_border[i];
        }
    }

    cout << ans << '\n';
    return 0;
}
