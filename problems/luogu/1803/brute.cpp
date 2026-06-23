// brute.cpp：小数据暴力解，用来帮助理解题意并辅助对拍。
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 25;

struct Segment {
    int l;
    int r;
};

int n;
Segment seg[MAXN];

bool cmp_segment(const Segment &a, const Segment &b) {
    if (a.l != b.l) {
        return a.l < b.l;
    }
    return a.r < b.r;
}

bool check_subset(int mask) {
    vector<Segment> chosen;
    for (int i = 0; i < n; i++) {
        if (mask & (1 << i)) {
            chosen.push_back(seg[i]);
        }
    }

    sort(chosen.begin(), chosen.end(), cmp_segment);
    for (int i = 1; i < (int)chosen.size(); i++) {
        if (chosen[i].l < chosen[i - 1].r) {
            return false;
        }
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> seg[i].l >> seg[i].r;
    }

    int ans = 0;
    for (int mask = 0; mask < (1 << n); mask++) {
        if (check_subset(mask)) {
            ans = max(ans, __builtin_popcount((unsigned)mask));
        }
    }

    cout << ans << '\n';
    return 0;
}
