#include <bits/stdc++.h>
using namespace std;

int n;
vector<int> iq, eq;
int answer = 0;

// 暴力枚举每头奶牛选或不选。
// 这个做法只适合小数据，但能直接对应题意。
void dfs(int idx, int sum_iq, int sum_eq) {
    if (idx == n) {
        if (sum_iq >= 0 && sum_eq >= 0) {
            answer = max(answer, sum_iq + sum_eq);
        }
        return;
    }

    // 不选这头牛。
    dfs(idx + 1, sum_iq, sum_eq);

    // 选这头牛。
    dfs(idx + 1, sum_iq + iq[idx], sum_eq + eq[idx]);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    iq.resize(n);
    eq.resize(n);
    for (int i = 0; i < n; i++) {
        cin >> iq[i] >> eq[i];
    }

    dfs(0, 0, 0);
    cout << answer << '\n';

    return 0;
}
