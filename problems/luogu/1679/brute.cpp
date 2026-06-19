#include <bits/stdc++.h>
using namespace std;

// brute.cpp：小数据暴力解，用来帮助理解题意并辅助对拍。

const int INF = 1e9;

int m;
vector<int> pows;
int answer = INF;

// 依次枚举每种四次方数要用多少个。
// 复杂度很高，只适合小数据验证。
void dfs(int idx, int remain, int used_cnt) {
    if (used_cnt >= answer) {
        return;
    }
    if (idx == (int)pows.size()) {
        if (remain == 0) {
            answer = min(answer, used_cnt);
        }
        return;
    }

    int w = pows[idx];
    int limit = remain / w;
    for (int cnt = 0; cnt <= limit; cnt++) {
        dfs(idx + 1, remain - cnt * w, used_cnt + cnt);
    }
}

void read_input() {
    cin >> m;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_input();
    for (int i = 1; ; i++) {
        long long x = 1LL * i * i * i * i;
        if (x > m) {
            break;
        }
        pows.push_back((int)x);
    }

    dfs(0, m, 0);
    cout << answer << '\n';

    return 0;
}
