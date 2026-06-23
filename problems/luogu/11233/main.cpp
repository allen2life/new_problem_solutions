#include <bits/stdc++.h>
using namespace std;

const int MAXN = 200005;
const int MAXV = 1000005;
const long long NEG = -(long long)4e18;

int T, n;
int a[MAXN];
bool active_state[MAXV];
long long dp[MAXV]; // dp[x] 表示另一种颜色最后一个数为 x 时的最优得分，统一减去 lazy
long long lazy_add;
multiset<long long> values;
vector<int> touched;

long long get_actual(int x) {
    if (!active_state[x]) {
        return NEG;
    }
    return dp[x] + lazy_add;
}

long long get_max_except(int x) {
    if (values.empty()) {
        return NEG;
    }
    if (!active_state[x]) {
        return *values.rbegin() + lazy_add;
    }

    auto it = values.find(dp[x]);
    values.erase(it);

    long long ret = NEG;
    if (!values.empty()) {
        ret = *values.rbegin() + lazy_add;
    }

    values.insert(dp[x]);
    return ret;
}

void set_state(int x, long long actual_value) {
    if (active_state[x]) {
        auto it = values.find(dp[x]);
        values.erase(it);
    } else {
        active_state[x] = true;
        touched.push_back(x);
    }

    dp[x] = actual_value - lazy_add;
    values.insert(dp[x]);
}

void clear_case() {
    for (int i = 0; i < (int)touched.size(); i++) {
        active_state[touched[i]] = false;
        dp[touched[i]] = 0;
    }
    touched.clear();
    values.clear();
    lazy_add = 0;
}

void solve_one() {
    cin >> n;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    clear_case();

    int last_value = a[1];
    set_state(0, 0);

    for (int i = 2; i <= n; i++) {
        int x = a[i];

        // 当前数染到“另一种颜色”时，新的另一色最后值会变成 last_value。
        long long candidate = get_max_except(x);
        if (active_state[x]) {
            candidate = max(candidate, get_actual(x) + x);
        }

        // 当前数染到和上一个数相同的颜色，所有状态都会得到这一段相邻相同的贡献。
        if (x == last_value) {
            lazy_add += x;
        }

        long long current = get_actual(last_value);
        if (candidate > current) {
            set_state(last_value, candidate);
        }

        last_value = x;
    }

    long long ans = NEG;
    if (!values.empty()) {
        ans = *values.rbegin() + lazy_add;
    }
    cout << ans << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> T;
    while (T--) {
        solve_one();
    }

    return 0;
}
