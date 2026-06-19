#include <bits/stdc++.h>
using namespace std;

struct Block {
    int h;
    int c;
    int a;
};

int n;
vector<Block> blocks;
int answer = 0;

// 暴力枚举每种方块用了多少次。
// 这个做法只适合小数据，但最容易直接对应题意。
void dfs(int idx, int cur_height) {
    if (idx == n) {
        answer = max(answer, cur_height);
        return;
    }

    const auto &blk = blocks[idx];
    for (int cnt = 0; cnt <= blk.c; cnt++) {
        int next_height = cur_height + cnt * blk.h;
        if (next_height > blk.a) {
            break;
        }
        dfs(idx + 1, next_height);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    blocks.resize(n);
    for (int i = 0; i < n; i++) {
        cin >> blocks[i].h >> blocks[i].a >> blocks[i].c;
    }

    sort(blocks.begin(), blocks.end(), [](const Block &x, const Block &y) {
        return x.a < y.a;
    });

    dfs(0, 0);
    cout << answer << '\n';

    return 0;
}
