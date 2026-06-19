#include <bits/stdc++.h>
using namespace std;

struct Item {
    int t;
    int f;
    int h;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int D, G;
    cin >> D >> G;

    vector<Item> a(G);
    for (int i = 0; i < G; ++i) {
        cin >> a[i].t >> a[i].f >> a[i].h;
    }

    sort(a.begin(), a.end(), [](const Item &x, const Item &y) {
        return x.t < y.t;
    });

    vector<int> dp(D + 1, -1);
    dp[0] = 10;

    for (const auto &it : a) {
        vector<int> ndp = dp;
        for (int h = 0; h <= D; ++h) {
            if (dp[h] < it.t) {
                continue;
            }

            // 吃掉这个垃圾，生命时间增加。
            ndp[h] = max(ndp[h], dp[h] + it.f);

            // 把这个垃圾堆起来，高度增加。
            int nh = min(D, h + it.h);
            ndp[nh] = max(ndp[nh], dp[h]);
        }

        dp.swap(ndp);

        // 一旦高度达到 D，就可以立刻逃出。
        if (dp[D] >= it.t) {
            cout << it.t << '\n';
            return 0;
        }
    }

    cout << *max_element(dp.begin(), dp.end()) << '\n';
    return 0;
}
