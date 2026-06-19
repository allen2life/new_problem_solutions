#include <bits/stdc++.h>
using namespace std;

const int MOD = 1000007;

int n, m;
vector<int> a;
int answer = 0;

// 暴力枚举每种花选多少盆。
// 对于小数据，这个做法最直观，也最容易对应题意。
void dfs(int idx, int remain) {
    if (idx == n) {
        if (remain == 0) {
            answer++;
            if (answer >= MOD) answer -= MOD;
        }
        return;
    }

    for (int cnt = 0; cnt <= a[idx] && cnt <= remain; cnt++) {
        dfs(idx + 1, remain - cnt);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m;
    a.resize(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    dfs(0, m);
    cout << answer << '\n';

    return 0;
}
