#include <bits/stdc++.h>
using namespace std;

const int MAXN = 8000 + 5;

int n, q;
int a[MAXN];
vector<pair<int, int> > ord;

int get_pos(pair<int, int> x) {
    return (int) (lower_bound(ord.begin(), ord.end(), x) - ord.begin());
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> q;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        ord.push_back(make_pair(a[i], i));
    }
    sort(ord.begin(), ord.end());

    while (q--) {
        int op;
        cin >> op;

        if (op == 1) {
            int x, v;
            cin >> x >> v;

            pair<int, int> old_node = make_pair(a[x], x);
            int old_pos = get_pos(old_node);
            ord.erase(ord.begin() + old_pos);

            a[x] = v;
            pair<int, int> new_node = make_pair(a[x], x);
            int new_pos = (int) (lower_bound(ord.begin(), ord.end(), new_node) - ord.begin());
            ord.insert(ord.begin() + new_pos, new_node);
        }
        else {
            int x;
            cin >> x;
            cout << get_pos(make_pair(a[x], x)) + 1 << '\n';
        }
    }

    return 0;
}
