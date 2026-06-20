#include <bits/stdc++.h>
using namespace std;

const int MAXN = 25;

struct Edge {
    int to;
    int w;
};

int n, k_need;
vector<Edge> g[MAXN];
int dista[MAXN][MAXN];
int choose_black[MAXN];
long long ans;

void dfs_dist(int start, int u, int fa, int d) {
    dista[start][u] = d;
    for (size_t i = 0; i < g[u].size(); i++) {
        int v = g[u][i].to;
        int w = g[u][i].w;
        if (v == fa) {
            continue;
        }
        dfs_dist(start, v, u, d + w);
    }
}

void dfs_choose(int u, int chosen) {
    if (chosen > k_need) {
        return;
    }
    if (u == n + 1) {
        if (chosen != k_need) {
            return;
        }

        long long sum = 0;
        for (int i = 1; i <= n; i++) {
            for (int j = i + 1; j <= n; j++) {
                if (choose_black[i] == choose_black[j]) {
                    sum += dista[i][j];
                }
            }
        }
        ans = max(ans, sum);
        return;
    }

    choose_black[u] = 0;
    dfs_choose(u + 1, chosen);
    choose_black[u] = 1;
    dfs_choose(u + 1, chosen + 1);
    choose_black[u] = 0;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // brute.cpp：枚举哪些点染成黑色，直接统计黑黑点对和白白点对的距离和。
    cin >> n >> k_need;
    for (int i = 1; i <= n; i++) {
        g[i].clear();
    }
    for (int i = 1; i < n; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        g[v].push_back({u, w});
    }

    for (int i = 1; i <= n; i++) {
        dfs_dist(i, i, 0, 0);
    }

    ans = 0;
    dfs_choose(1, 0);
    cout << ans << '\n';
    return 0;
}
