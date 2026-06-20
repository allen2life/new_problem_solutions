#include <bits/stdc++.h>
using namespace std;

const int MAXN = 15;

struct Edge {
    int u, v, w;
};

int n, q_need;
Edge edges[MAXN];
vector<pair<int, int> > g[MAXN];
int chosen[MAXN];
int ans;

void dfs_choose(int idx, int picked) {
    if (picked > q_need) {
        return;
    }
    if (idx == n) {
        if (picked != q_need) {
            return;
        }

        vector<int> vis(n + 1, 0);
        queue<int> q;
        q.push(1);
        vis[1] = 1;
        int sum = 0;

        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (size_t i = 0; i < g[u].size(); i++) {
                int id = g[u][i].second;
                int v = g[u][i].first;
                if (!chosen[id] || vis[v]) {
                    continue;
                }
                vis[v] = 1;
                sum += edges[id].w;
                q.push(v);
            }
        }

        int real_edges = 0;
        for (int i = 1; i < n; i++) {
            if (chosen[i]) {
                real_edges++;
            }
        }
        if (sum > ans && real_edges == q_need) {
            // 由于是树，只要选出的边都和根连通，就一定恰好留下这些边上的苹果。
            ans = sum;
        }
        return;
    }

    chosen[idx] = 0;
    dfs_choose(idx + 1, picked);
    chosen[idx] = 1;
    dfs_choose(idx + 1, picked + 1);
    chosen[idx] = 0;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // brute.cpp：枚举保留哪些边，再检查这些边是否仍然和根连通。
    cin >> n >> q_need;
    for (int i = 1; i <= n; i++) {
        g[i].clear();
    }

    for (int i = 1; i < n; i++) {
        cin >> edges[i].u >> edges[i].v >> edges[i].w;
        g[edges[i].u].push_back({edges[i].v, i});
        g[edges[i].v].push_back({edges[i].u, i});
        chosen[i] = 0;
    }

    ans = 0;
    dfs_choose(1, 0);
    cout << ans << '\n';
    return 0;
}
