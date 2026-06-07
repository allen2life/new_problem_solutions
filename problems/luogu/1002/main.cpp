#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const int MAXN = 25;

int n, m, hx, hy;
ll dp[MAXN][MAXN];
bool blocked[MAXN][MAXN];

int dx[] = {0, 1, 1, -1, -1, 2, 2, -2, -2};
int dy[] = {0, 2, -2, 2, -2, 1, -1, 1, -1};

bool in_board(int x, int y) {
    return x >= 0 && x <= n && y >= 0 && y <= m;
}

void mark_horse() {
    for (int i = 0; i < 9; i++) {
        int nx = hx + dx[i];
        int ny = hy + dy[i];
        if (in_board(nx, ny)) {
            blocked[nx][ny] = true;
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m >> hx >> hy;
    mark_horse();

    if (!blocked[0][0]) dp[0][0] = 1;
    for (int i = 0; i <= n; i++) {
        for (int j = 0; j <= m; j++) {
            if (blocked[i][j]) {
                dp[i][j] = 0;
                continue;
            }
            if (i > 0) dp[i][j] += dp[i - 1][j];
            if (j > 0) dp[i][j] += dp[i][j - 1];
        }
    }

    cout << dp[n][m] << '\n';
    return 0;
}
