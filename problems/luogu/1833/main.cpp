#include <bits/stdc++.h>
using namespace std;

static int parse_time(const string &s) {
    size_t pos = s.find(':');
    int h = stoi(s.substr(0, pos));
    int m = stoi(s.substr(pos + 1));
    return h * 60 + m;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string start_s, end_s;
    int n;
    if (!(cin >> start_s >> end_s >> n)) {
        return 0;
    }

    int limit = parse_time(end_s) - parse_time(start_s);
    if (limit < 0) {
        limit += 24 * 60;
    }

    vector<int> dp(limit + 1, 0);

    for (int i = 0; i < n; ++i) {
        int t, c, p;
        cin >> t >> c >> p;

        if (t > limit) {
            continue;
        }

        if (p == 0) {
            // 无限次：完全背包，容量正序。
            for (int j = t; j <= limit; ++j) {
                dp[j] = max(dp[j], dp[j - t] + c);
            }
        } else {
            // 有上限：二进制拆分成若干个 0/1 物品。
            int k = 1;
            int rest = p;
            while (rest > 0) {
                int take = min(k, rest);
                int wt = take * t;
                int val = take * c;
                if (wt <= limit) {
                    for (int j = limit; j >= wt; --j) {
                        dp[j] = max(dp[j], dp[j - wt] + val);
                    }
                }
                rest -= take;
                k <<= 1;
            }
        }
    }

    cout << dp[limit] << '\n';
    return 0;
}
