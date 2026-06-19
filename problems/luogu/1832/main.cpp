#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1005;

int n;
bool is_prime[MAXN];
vector<int> primes;
vector<long long> dp; // dp[j] 表示凑出 j 的组合方案数

void build_primes() {
    for (int i = 2; i <= n; i++) {
        if (!is_prime[i]) {
            primes.push_back(i);
            for (int j = i + i; j <= n; j += i) {
                is_prime[j] = true;
            }
        }
    }
}

void read_input() {
    cin >> n;
}

void solve() {
    build_primes();

    dp.assign(n + 1, 0);
    dp[0] = 1;

    for (int i = 0; i < (int)primes.size(); i++) {
        int p = primes[i];
        // 完全背包计数：正序枚举，统计“组合数”而不是“排列数”。
        for (int j = p; j <= n; j++) {
            dp[j] += dp[j - p];
        }
    }

    cout << dp[n] << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_input();
    solve();

    return 0;
}
