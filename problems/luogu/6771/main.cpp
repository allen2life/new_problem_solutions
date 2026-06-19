#include <bits/stdc++.h>
using namespace std;

struct Block {
    int h; // 方块高度
    int c; // 数量
    int a; // 允许到达的最高高度
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<Block> blocks(n);
    int max_a = 0;
    for (int i = 0; i < n; i++) {
        cin >> blocks[i].h >> blocks[i].a >> blocks[i].c;
        max_a = max(max_a, blocks[i].a);
    }

    sort(blocks.begin(), blocks.end(), [](const Block &x, const Block &y) {
        return x.a < y.a;
    });

    // dp[h] = 当前能否堆出高度 h。
    vector<char> dp(max_a + 1, 0);
    dp[0] = 1;

    for (const auto &blk : blocks) {
        if (blk.h > blk.a) {
            continue;
        }

        // 每种方块最多使用 c 次，所以重复做 c 次 0/1 转移。
        for (int t = 0; t < blk.c; t++) {
            for (int h = blk.a - blk.h; h >= 0; h--) {
                if (!dp[h]) continue;
                dp[h + blk.h] = 1;
            }
        }
    }

    for (int h = max_a; h >= 0; h--) {
        if (dp[h]) {
            cout << h << '\n';
            break;
        }
    }

    return 0;
}
