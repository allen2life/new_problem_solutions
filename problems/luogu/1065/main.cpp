#include <bits/stdc++.h>
using namespace std;

const int MAXM = 25;
const int MAXN = 25;
const int MAXT = 10005;

int m, n;
int order_list[MAXM * MAXN];
int machine_id[MAXN][MAXM];
int cost_time[MAXN][MAXM];
int next_step[MAXN];      // 当前工件下一次要安排的是第几道工序
int finish_time[MAXN];    // 当前工件已经安排完成的最后时间
bool used[MAXM][MAXT];    // used[machine][time] 表示该机器在该时刻是否被占用

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> m >> n;
    int tot = m * n;

    for (int i = 1; i <= tot; i++) {
        cin >> order_list[i];
    }

    for (int job = 1; job <= n; job++) {
        for (int step = 1; step <= m; step++) {
            cin >> machine_id[job][step];
        }
    }

    for (int job = 1; job <= n; job++) {
        for (int step = 1; step <= m; step++) {
            cin >> cost_time[job][step];
        }
    }

    int answer = 0;

    for (int idx = 1; idx <= tot; idx++) {
        int job = order_list[idx];
        int step = ++next_step[job];
        int mac = machine_id[job][step];
        int len = cost_time[job][step];

        int start = finish_time[job];

        while (true) {
            bool ok = true;
            for (int t = start; t < start + len; t++) {
                if (used[mac][t]) {
                    start = t + 1;
                    ok = false;
                    break;
                }
            }
            if (ok) {
                break;
            }
        }

        for (int t = start; t < start + len; t++) {
            used[mac][t] = true;
        }

        finish_time[job] = start + len;
        answer = max(answer, finish_time[job]);
    }

    cout << answer << '\n';
    return 0;
}
