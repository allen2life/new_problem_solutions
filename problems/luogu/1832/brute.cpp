#include <bits/stdc++.h>
using namespace std;

// brute.cpp：小数据暴力解，用来帮助理解题意并辅助对拍。

const int MAXN = 1005;

int n;
bool is_prime[MAXN];
vector<int> primes;
long long answer;

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

// 依次枚举每个素数用了多少次。
// 复杂度很高，只适合小数据验证。
void dfs(int idx, int remain) {
    if (idx == (int)primes.size()) {
        if (remain == 0) {
            answer++;
        }
        return;
    }

    int p = primes[idx];
    int limit = remain / p;
    for (int cnt = 0; cnt <= limit; cnt++) {
        dfs(idx + 1, remain - cnt * p);
    }
}

void read_input() {
    cin >> n;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_input();
    build_primes();
    dfs(0, n);
    cout << answer << '\n';

    return 0;
}
