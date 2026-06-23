#include <bits/stdc++.h>
using namespace std;

const int MAXN = 2005;

int t, k;
int comb_mod[MAXN][MAXN]; // comb_mod[i][j] 保存 C(i,j) mod k。
int bad[MAXN][MAXN];      // bad[i][j]=1 表示 k 能整除 C(i,j)。
int prefix_bad[MAXN][MAXN]; // 二维前缀和，快速回答 0<=j<=min(i,m) 的数量。

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> t >> k;

    comb_mod[0][0] = 1 % k;
    for (int i = 1; i < MAXN; i++) {
        comb_mod[i][0] = comb_mod[i][i] = 1 % k;
        for (int j = 1; j < i; j++) {
            comb_mod[i][j] = (comb_mod[i - 1][j - 1] + comb_mod[i - 1][j]) % k;
        }
    }

    for (int i = 0; i < MAXN; i++) {
        for (int j = 0; j <= i; j++) {
            if (comb_mod[i][j] == 0) {
                bad[i][j] = 1;
            }
        }
    }

    for (int i = 0; i < MAXN; i++) {
        for (int j = 0; j < MAXN; j++) {
            int up = (i > 0 ? prefix_bad[i - 1][j] : 0);
            int left = (j > 0 ? prefix_bad[i][j - 1] : 0);
            int diag = (i > 0 && j > 0 ? prefix_bad[i - 1][j - 1] : 0);
            prefix_bad[i][j] = up + left - diag + bad[i][j];
        }
    }

    while (t--) {
        int n, m;
        cin >> n >> m;
        if (m > n) {
            m = n;
        }
        cout << prefix_bad[n][m] << '\n';
    }

    return 0;
}
