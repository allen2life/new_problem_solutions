#include <bits/stdc++.h>
using namespace std;

const int MAXNODE = 150005;

int n;
int trie[MAXNODE][26];
bool is_word[MAXNODE];
int node_cnt;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;

    int ans = 0;

    for (int i = 1; i <= n; i++) {
        string s;
        cin >> s;

        int u = 0;
        int chain_len = 0;

        for (int j = 0; j < (int)s.size(); j++) {
            int c = s[j] - 'a';
            if (trie[u][c] == 0) {
                trie[u][c] = ++node_cnt;
            }
            u = trie[u][c];

            // 路径上已经结束的单词，都是当前单词的前缀。
            if (is_word[u]) {
                chain_len++;
            }
        }

        // 当前单词自己也要算进词链长度。
        chain_len++;
        is_word[u] = true;

        ans = max(ans, chain_len);
    }

    cout << ans << '\n';
    return 0;
}
