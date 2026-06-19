#include <bits/stdc++.h>
using namespace std;

const int MAXN = 205;

int n, s, t;
int k[MAXN];
int dista[MAXN];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> s >> t;
    for (int i = 1; i <= n; i++) {
        cin >> k[i];
    }

    memset(dista, -1, sizeof(dista));
    queue<int> q;
    dista[s] = 0;
    q.push(s);

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        if (u == t) {
            cout << dista[u] << '\n';
            return 0;
        }

        int v1 = u + k[u];
        int v2 = u - k[u];

        if (v1 >= 1 && v1 <= n && dista[v1] == -1) {
            dista[v1] = dista[u] + 1;
            q.push(v1);
        }
        if (v2 >= 1 && v2 <= n && dista[v2] == -1) {
            dista[v2] = dista[u] + 1;
            q.push(v2);
        }
    }

    cout << -1 << '\n';
    return 0;
}
