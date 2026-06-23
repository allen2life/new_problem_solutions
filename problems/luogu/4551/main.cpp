#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
const int MAXNODE = MAXN * 32;

int n;
int head[MAXN], to[MAXN * 2], nxt[MAXN * 2], edge_cnt;
unsigned int weight_edge[MAXN * 2];
unsigned int xor_root[MAXN];

int trie[MAXNODE][2], trie_cnt;

void add_edge(int u, int v, unsigned int w) {
    edge_cnt++;
    to[edge_cnt] = v;
    weight_edge[edge_cnt] = w;
    nxt[edge_cnt] = head[u];
    head[u] = edge_cnt;
}

void read_input() {
    cin >> n;
    for (int i = 1; i < n; i++) {
        int u, v;
        unsigned int w;
        cin >> u >> v >> w;
        add_edge(u, v, w);
        add_edge(v, u, w);
    }
}

void calc_xor_values() {
    queue<int> que;
    vector<int> parent(n + 1, 0);
    que.push(1);
    parent[1] = -1;
    xor_root[1] = 0;

    while (!que.empty()) {
        int u = que.front();
        que.pop();

        for (int i = head[u]; i != 0; i = nxt[i]) {
            int v = to[i];
            if (v == parent[u]) {
                continue;
            }
            parent[v] = u;
            xor_root[v] = xor_root[u] ^ weight_edge[i];
            que.push(v);
        }
    }
}

void trie_insert(unsigned int x) {
    int p = 0;
    for (int bit = 30; bit >= 0; bit--) {
        int c = (x >> bit) & 1U;
        if (trie[p][c] == 0) {
            trie_cnt++;
            trie[p][c] = trie_cnt;
        }
        p = trie[p][c];
    }
}

unsigned int trie_query(unsigned int x) {
    int p = 0;
    unsigned int answer = 0;
    for (int bit = 30; bit >= 0; bit--) {
        int c = (x >> bit) & 1U;
        int want = c ^ 1;
        if (trie[p][want] != 0) {
            answer |= (1U << bit);
            p = trie[p][want];
        } else {
            p = trie[p][c];
        }
    }
    return answer;
}

void solve() {
    calc_xor_values();

    unsigned int answer = 0;
    trie_insert(xor_root[1]);
    for (int i = 2; i <= n; i++) {
        answer = max(answer, trie_query(xor_root[i]));
        trie_insert(xor_root[i]);
    }

    cout << answer << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_input();
    solve();

    return 0;
}
