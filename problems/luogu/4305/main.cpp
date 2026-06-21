#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        int n;
        cin >> n;

        set<int> vis;
        bool first = true;

        for (int i = 1; i <= n; i++) {
            int x;
            cin >> x;
            if (vis.count(x)) {
                continue;
            }
            vis.insert(x);

            if (!first) {
                cout << ' ';
            }
            cout << x;
            first = false;
        }
        cout << '\n';
    }

    return 0;
}
