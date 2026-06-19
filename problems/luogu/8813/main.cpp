#include <bits/stdc++.h>
using namespace std;

using ll = long long;

const ll LIMIT = 1000000000LL;

ll a, b;

// 安全乘法：一旦结果超过 LIMIT，就直接返回 LIMIT+1 作为超界标记。
ll multiply_with_cap(ll x, ll y) {
    if (x == 0 || y == 0) {
        return 0;
    }
    if (x > LIMIT / y) {
        return LIMIT + 1;
    }
    return x * y;
}

void solve() {
    ll ans = 1;
    ll base = a;
    ll exp = b;

    while (exp > 0) {
        if (exp & 1) {
            ans = multiply_with_cap(ans, base);
            if (ans > LIMIT) {
                cout << -1 << '\n';
                return;
            }
        }

        exp >>= 1;
        if (exp == 0) {
            break;
        }

        base = multiply_with_cap(base, base);
        if (base > LIMIT) {
            base = LIMIT + 1;
        }
    }

    cout << ans << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> a >> b;
    solve();

    return 0;
}
