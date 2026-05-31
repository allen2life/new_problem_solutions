#include <bits/stdc++.h>
using namespace std;

const int N = 2005;
int a[N];
int dp[N];   // dp[i]: 以 i 结尾的最长上升子序列长度
long long cnt[N]; // cnt[i]: 达到 dp[i] 长度的方案数

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        int n;
        cin >> n;
        for (int i = 0; i < n; i++) {
            cin >> a[i];
            dp[i] = 1;   // 每个元素自身构成长度为 1 的子序列
            cnt[i] = 1;  // 方案数为 1
        }

        int max_len = 1;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (a[j] < a[i]) { // 严格上升
                    if (dp[j] + 1 > dp[i]) {
                        // 找到了更长的子序列，更新长度和方案数
                        dp[i] = dp[j] + 1;
                        cnt[i] = cnt[j];
                    } else if (dp[j] + 1 == dp[i]) {
                        // 同样长度的子序列，累加方案数
                        cnt[i] += cnt[j];
                    }
                }
            }
            max_len = max(max_len, dp[i]);
        }

        // 统计所有达到最长长度的方案数
        long long total = 0;
        for (int i = 0; i < n; i++) {
            if (dp[i] == max_len) {
                total += cnt[i];
            }
        }

        cout << max_len << " " << total << "\n";
    }

    return 0;
}
