#include <bits/stdc++.h>
using namespace std;

// brute.cpp：枚举所有课程集合，检查先修约束，只适合小数据。

const int MAXN = 25;

int n, m;
int parent_course[MAXN];
int credit[MAXN];
int choose_flag[MAXN];
int answer;

void dfs_enum(int pos, int chosen_count) {
    if (pos == n + 1) {
        if (chosen_count != m) {
            return;
        }

        for (int i = 1; i <= n; i++) {
            if (choose_flag[i] && parent_course[i] != 0 && !choose_flag[parent_course[i]]) {
                return;
            }
        }

        int sum = 0;
        for (int i = 1; i <= n; i++) {
            if (choose_flag[i]) {
                sum += credit[i];
            }
        }
        answer = max(answer, sum);
        return;
    }

    choose_flag[pos] = 0;
    dfs_enum(pos + 1, chosen_count);

    choose_flag[pos] = 1;
    dfs_enum(pos + 1, chosen_count + 1);
    choose_flag[pos] = 0;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        cin >> parent_course[i] >> credit[i];
    }

    answer = 0;
    dfs_enum(1, 0);
    cout << answer << '\n';

    return 0;
}
