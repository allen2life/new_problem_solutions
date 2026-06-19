#include <bits/stdc++.h>
using namespace std;

struct State {
    int cnt;   // 能泡到的 MM 数量
    int time;  // 在该数量下的最少时间
};

static inline bool better(const State &a, const State &b) {
    if (a.cnt != b.cnt) return a.cnt > b.cnt;
    return a.time < b.time;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<array<int, 3>> girl(n);
    for (int i = 0; i < n; i++) {
        cin >> girl[i][0] >> girl[i][1] >> girl[i][2];
    }

    int money, rp;
    cin >> money >> rp;

    // dp[j][k]：在钱不超过 j、人品不超过 k 的前提下，最多能泡到多少 MM，
    //          如果数量相同，则取时间更少的方案。
    vector<vector<State>> dp(money + 1, vector<State>(rp + 1, {0, 0}));

    for (int i = 0; i < n; i++) {
        int need_money = girl[i][0];
        int need_rp = girl[i][1];
        int need_time = girl[i][2];

        // 0/1 背包：每个 MM 只能泡一次，所以容量倒序。
        for (int j = money; j >= need_money; j--) {
            for (int k = rp; k >= need_rp; k--) {
                State cand = dp[j - need_money][k - need_rp];
                cand.cnt++;
                cand.time += need_time;
                if (better(cand, dp[j][k])) {
                    dp[j][k] = cand;
                }
            }
        }
    }

    cout << dp[money][rp].time << '\n';

    return 0;
}
