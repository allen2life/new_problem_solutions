#include <bits/stdc++.h>
using namespace std;

struct Item {
    int value;
    int weight;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, capacity;
    cin >> n >> capacity;

    vector<Item> items;
    items.reserve(2000);

    for (int i = 1; i <= n; ++i) {
        int value, weight, count;
        cin >> value >> weight >> count;

        // 把 count 件物品拆成 1,2,4,... 的若干组，转成 0/1 背包。
        for (int k = 1; k <= count; k <<= 1) {
            items.push_back({value * k, weight * k});
            count -= k;
        }
        if (count > 0) {
            items.push_back({value * count, weight * count});
        }
    }

    vector<int> dp(capacity + 1, 0);
    for (const auto &item : items) {
        for (int j = capacity; j >= item.weight; --j) {
            dp[j] = max(dp[j], dp[j - item.weight] + item.value);
        }
    }

    cout << dp[capacity] << '\n';
    return 0;
}
