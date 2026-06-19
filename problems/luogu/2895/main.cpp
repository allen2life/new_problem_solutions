#include <bits/stdc++.h>
using namespace std;

const int LIM = 310;
const int INF = 0x3f3f3f3f;

int m;
int danger_time[LIM][LIM];
int dista[LIM][LIM];
int dx[5] = {0, 1, -1, 0, 0};
int dy[5] = {0, 0, 0, 1, -1};

struct Node {
    int x;
    int y;
};

bool in_board(int x, int y) {
    return x >= 0 && x < LIM && y >= 0 && y < LIM;
}

int bfs() {
    if (danger_time[0][0] == 0) {
        return -1;
    }

    queue<Node> q;
    memset(dista, -1, sizeof(dista));
    dista[0][0] = 0;
    q.push((Node){0, 0});

    while (!q.empty()) {
        Node u = q.front();
        q.pop();

        if (danger_time[u.x][u.y] == INF) {
            return dista[u.x][u.y];
        }

        for (int i = 1; i <= 4; i++) {
            int nx = u.x + dx[i];
            int ny = u.y + dy[i];
            int nt = dista[u.x][u.y] + 1;

            if (!in_board(nx, ny)) {
                continue;
            }
            if (dista[nx][ny] != -1) {
                continue;
            }
            if (nt >= danger_time[nx][ny]) {
                continue;
            }

            dista[nx][ny] = nt;
            q.push((Node){nx, ny});
        }
    }

    return -1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> m;

    for (int i = 0; i < LIM; i++) {
        for (int j = 0; j < LIM; j++) {
            danger_time[i][j] = INF;
        }
    }

    for (int i = 1; i <= m; i++) {
        int x, y, t;
        cin >> x >> y >> t;

        for (int j = 0; j <= 4; j++) {
            int nx = x + dx[j];
            int ny = y + dy[j];
            if (!in_board(nx, ny)) {
                continue;
            }
            danger_time[nx][ny] = min(danger_time[nx][ny], t);
        }
    }

    cout << bfs() << '\n';
    return 0;
}
