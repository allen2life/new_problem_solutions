#include <bits/stdc++.h>
using namespace std;

struct Girl {
    int money;
    int rp;
    int time;
};

int n, money, rp;
vector<Girl> girls;
int best_cnt = 0;
int best_time = 0;

// 暴力枚举每个 MM 选或不选。
// 这个做法只适合小数据，但能直接对应题意。
void dfs(int idx, int cur_money, int cur_rp, int cur_cnt, int cur_time) {
    if (cur_money > money || cur_rp > rp) {
        return;
    }

    if (idx == n) {
        if (cur_cnt > best_cnt || (cur_cnt == best_cnt && cur_time < best_time)) {
            best_cnt = cur_cnt;
            best_time = cur_time;
        }
        return;
    }

    // 不选第 idx 个 MM。
    dfs(idx + 1, cur_money, cur_rp, cur_cnt, cur_time);

    // 选第 idx 个 MM。
    dfs(idx + 1,
        cur_money + girls[idx].money,
        cur_rp + girls[idx].rp,
        cur_cnt + 1,
        cur_time + girls[idx].time);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    girls.resize(n);
    for (int i = 0; i < n; i++) {
        cin >> girls[i].money >> girls[i].rp >> girls[i].time;
    }
    cin >> money >> rp;

    dfs(0, 0, 0, 0, 0);
    cout << best_time << '\n';

    return 0;
}
