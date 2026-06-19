#include <bits/stdc++.h>
using namespace std;

// brute.cpp：小数据暴力解，用来帮助理解题意并辅助对拍。

const int MAXH = 5005;

int c, h;
int volume[MAXH];
int answer;

// 枚举每捆草买或不买。
// 复杂度是 O(2^h)，只适合小数据验证。
void dfs(int idx, int total_volume) {
    if (total_volume > c) {
        return;
    }
    if (idx > h) {
        answer = max(answer, total_volume);
        return;
    }

    dfs(idx + 1, total_volume);
    dfs(idx + 1, total_volume + volume[idx]);
}

void read_input() {
    cin >> c >> h;
    for (int i = 1; i <= h; i++) {
        cin >> volume[i];
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_input();
    dfs(1, 0);
    cout << answer << '\n';

    return 0;
}
