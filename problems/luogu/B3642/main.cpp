#include <bits/stdc++.h>
using namespace std;

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

    vector<int> left_son(n + 1), right_son(n + 1);
    for (int i = 1; i <= n; ++i) {
        cin >> left_son[i] >> right_son[i];
    }

    vector<int> preorder;
    vector<int> inorder;
    vector<int> postorder;
    preorder.reserve(n);
    inorder.reserve(n);
    postorder.reserve(n);

    // 前序：根 -> 左 -> 右。
    vector<int> st;
    st.push_back(1);
    while (!st.empty()) {
        int u = st.back();
        st.pop_back();
        if (u == 0) {
            continue;
        }
        preorder.push_back(u);
        if (right_son[u] != 0) {
            st.push_back(right_son[u]);
        }
        if (left_son[u] != 0) {
            st.push_back(left_son[u]);
        }
    }

    // 中序：左 -> 根 -> 右。
    st.clear();
    int cur = 1;
    while (cur != 0 || !st.empty()) {
        while (cur != 0) {
            st.push_back(cur);
            cur = left_son[cur];
        }
        cur = st.back();
        st.pop_back();
        inorder.push_back(cur);
        cur = right_son[cur];
    }

    // 后序：左 -> 右 -> 根。用双栈避免深递归。
    vector<int> st2;
    st.push_back(1);
    while (!st.empty()) {
        int u = st.back();
        st.pop_back();
        if (u == 0) {
            continue;
        }
        st2.push_back(u);
        if (left_son[u] != 0) {
            st.push_back(left_son[u]);
        }
        if (right_son[u] != 0) {
            st.push_back(right_son[u]);
        }
    }
    for (int i = (int)st2.size() - 1; i >= 0; --i) {
        postorder.push_back(st2[i]);
    }

    print_sequence(preorder);
    print_sequence(inorder);
    print_sequence(postorder);
    return 0;
}
