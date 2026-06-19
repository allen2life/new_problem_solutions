#include <bits/stdc++.h>
using namespace std;

enum NodeType {
    VAR_NODE = 0,
    NOT_NODE = 1,
    AND_NODE = 2,
    OR_NODE = 3,
};

struct Node {
    int type;
    int left;
    int right;
    int var_id;
    int value;
};

vector<string> split_tokens(const string &s) {
    vector<string> tokens;
    int n = (int)s.size();
    int i = 0;
    while (i < n) {
        while (i < n && s[i] == ' ') {
            ++i;
        }
        if (i >= n) {
            break;
        }
        int j = i;
        while (j < n && s[j] != ' ') {
            ++j;
        }
        tokens.push_back(s.substr(i, j - i));
        i = j;
    }
    return tokens;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string expr;
    getline(cin, expr);

    int n;
    cin >> n;
    vector<int> init_value(n + 1);
    for (int i = 1; i <= n; ++i) {
        cin >> init_value[i];
    }

    vector<string> tokens = split_tokens(expr);
    vector<Node> nodes(1);
    nodes.reserve(tokens.size() + 1);
    vector<int> st;
    st.reserve(tokens.size());
    vector<int> var_pos(n + 1, 0);

    for (const string &token : tokens) {
        if (token[0] == 'x') {
            int id = stoi(token.substr(1));
            nodes.push_back({VAR_NODE, 0, 0, id, init_value[id]});
            int node_id = (int)nodes.size() - 1;
            var_pos[id] = node_id;
            st.push_back(node_id);
        } else if (token == "!") {
            int child = st.back();
            st.pop_back();
            nodes.push_back({NOT_NODE, child, 0, 0, nodes[child].value ^ 1});
            st.push_back((int)nodes.size() - 1);
        } else {
            int right = st.back();
            st.pop_back();
            int left = st.back();
            st.pop_back();

            int value;
            if (token == "&") {
                value = nodes[left].value & nodes[right].value;
                nodes.push_back({AND_NODE, left, right, 0, value});
            } else {
                value = nodes[left].value | nodes[right].value;
                nodes.push_back({OR_NODE, left, right, 0, value});
            }
            st.push_back((int)nodes.size() - 1);
        }
    }

    int root = st.back();
    vector<char> can_affect(nodes.size(), 0);
    vector<int> dfs_stack;
    dfs_stack.push_back(root);
    can_affect[root] = 1;

    // 从根向下传播“这个子树改动后是否可能影响最终答案”。
    while (!dfs_stack.empty()) {
        int u = dfs_stack.back();
        dfs_stack.pop_back();

        if (nodes[u].type == VAR_NODE) {
            continue;
        }
        if (nodes[u].type == NOT_NODE) {
            int child = nodes[u].left;
            if (!can_affect[child]) {
                can_affect[child] = 1;
                dfs_stack.push_back(child);
            }
        } else if (nodes[u].type == AND_NODE) {
            int left = nodes[u].left;
            int right = nodes[u].right;

            if (nodes[right].value == 1 && !can_affect[left]) {
                can_affect[left] = 1;
                dfs_stack.push_back(left);
            }
            if (nodes[left].value == 1 && !can_affect[right]) {
                can_affect[right] = 1;
                dfs_stack.push_back(right);
            }
        } else {
            int left = nodes[u].left;
            int right = nodes[u].right;

            if (nodes[right].value == 0 && !can_affect[left]) {
                can_affect[left] = 1;
                dfs_stack.push_back(left);
            }
            if (nodes[left].value == 0 && !can_affect[right]) {
                can_affect[right] = 1;
                dfs_stack.push_back(right);
            }
        }
    }

    int q;
    cin >> q;
    int root_value = nodes[root].value;
    while (q--) {
        int x;
        cin >> x;
        if (can_affect[var_pos[x]]) {
            cout << (root_value ^ 1) << '\n';
        } else {
            cout << root_value << '\n';
        }
    }
    return 0;
}
