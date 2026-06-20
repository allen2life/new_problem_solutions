#include <bits/stdc++.h>
using namespace std;

const int MAXN = 22;

int n;
vector<int> g[MAXN];
int choose_tower[MAXN];
int ans;

void dfs_choose(int u, int picked) {
    if (picked >= ans) {
        return;
    }
    if (u == n + 1) {
        for (int i = 1; i <= n; i++) {
            bool covered = choose_tower[i];
            for (size_t j = 0; j < g[i].size(); j++) {
                if (choose_tower[g[i][j]]) {
                    covered = true;
                    break;
                }
            }
            if (!covered) {
                return;
            }
        }
        ans = min(ans, picked);
        return;
    }

    choose_tower[u] = 0;
    dfs_choose(u + 1, picked);
    choose_tower[u] = 1;
    dfs_choose(u + 1, picked + 1);
    choose_tower[u] = 0;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // brute.cpp：枚举哪些点放塔，直接检查是否覆盖整棵树。
    cin >> n;
    for (int i = 1; i <= n; i++) {
        g[i].clear();
        choose_tower[i] = 0;
    }
    for (int i = 1; i < n; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    ans = n;
    dfs_choose(1, 0);
    cout << ans << '\n';
    return 0;
}
