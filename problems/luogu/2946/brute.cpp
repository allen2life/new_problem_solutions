#include <bits/stdc++.h>
using namespace std;

const int MOD = 100000000;

int n, f;
vector<int> a;
int answer = 0;

// 暴力枚举每头牛选或不选。
// 这个做法只适合小数据，但能直接验证题意。
void dfs(int idx, int sum_mod, bool chosen) {
    if (idx == n) {
        if (chosen && sum_mod == 0) {
            answer++;
            if (answer >= MOD) {
                answer -= MOD;
            }
        }
        return;
    }

    // 不选第 idx 头牛。
    dfs(idx + 1, sum_mod, chosen);

    // 选第 idx 头牛一次。
    dfs(idx + 1, (sum_mod + a[idx]) % f, true);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> f;
    a.resize(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    dfs(0, 0, false);
    cout << answer % MOD << '\n';

    return 0;
}
