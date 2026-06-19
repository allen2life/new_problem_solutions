#include <bits/stdc++.h>
using namespace std;

static vector<int> left_son;
static vector<int> right_son;
static vector<int> preorder;
static vector<int> inorder;
static vector<int> postorder;

void dfs_pre(int u) {
    if (u == 0) {
        return;
    }
    preorder.push_back(u);
    dfs_pre(left_son[u]);
    dfs_pre(right_son[u]);
}

void dfs_in(int u) {
    if (u == 0) {
        return;
    }
    dfs_in(left_son[u]);
    inorder.push_back(u);
    dfs_in(right_son[u]);
}

void dfs_post(int u) {
    if (u == 0) {
        return;
    }
    dfs_post(left_son[u]);
    dfs_post(right_son[u]);
    postorder.push_back(u);
}

void print_sequence(const vector<int> &seq) {
    for (int i = 0; i < (int)seq.size(); ++i) {
        if (i) {
            cout << ' ';
        }
        cout << seq[i];
    }
    cout << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    left_son.assign(n + 1, 0);
    right_son.assign(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        cin >> left_son[i] >> right_son[i];
    }

    dfs_pre(1);
    dfs_in(1);
    dfs_post(1);

    print_sequence(preorder);
    print_sequence(inorder);
    print_sequence(postorder);
    return 0;
}
