#include <bits/stdc++.h>
using namespace std;

const int MAXL = 105;

struct LoopInfo {
    string var;       // 当前循环定义的变量名
    bool claimed;     // 这个变量名是否成功占用，供出栈时释放
    bool is_dead;     // 这一层循环是否一开始就不会执行
    bool add_power;   // 这一层是否会让复杂度多乘一个 n
};

int test_cnt;
int line_cnt;
string target_complexity;

bool used_var[256];
LoopInfo stk[MAXL];
int top_ptr;

int parse_target_power(const string &s) {
    if (s == "O(1)") return 0;
    if (s == "O(n)") return 1;

    int pos1 = s.find('^');
    int pos2 = s.find(')');
    int value = 0;
    for (int i = pos1 + 1; i < pos2; i++) {
        value = value * 10 + (s[i] - '0');
    }
    return value;
}

bool is_n(const string &s) {
    return s == "n";
}

int to_number(const string &s) {
    int value = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        value = value * 10 + (s[i] - '0');
    }
    return value;
}

// 返回值：
// 0 -> 常数循环
// 1 -> 这一层会贡献一个 n
// 2 -> 这一层根本不会执行
int get_loop_type(const string &x, const string &y) {
    bool x_is_n = is_n(x);
    bool y_is_n = is_n(y);

    if (!x_is_n && !y_is_n) {
        int lx = to_number(x);
        int ry = to_number(y);
        if (lx > ry) return 2;
        return 0;
    }

    if (!x_is_n && y_is_n) return 1;
    if (x_is_n && !y_is_n) return 2;

    // n 到 n 只执行 1 次，是常数循环。
    return 0;
}

// 返回值：
// -1 -> 语法错误 ERR
//  1 -> 复杂度匹配 Yes
//  0 -> 复杂度不匹配 No
int solve_one_case() {
    cin >> line_cnt >> target_complexity;

    memset(used_var, 0, sizeof(used_var));
    top_ptr = 0;

    int target_power = parse_target_power(target_complexity);
    int current_power = 0; // 当前活跃执行路径上的 O(n) 层数
    int max_power = 0;     // 程序所有可执行路径中出现过的最大层数
    int dead_depth = 0;    // 当前是否处在“不会执行”的循环内部
    bool has_error = false;

    for (int i = 1; i <= line_cnt; i++) {
        string op;
        cin >> op;

        if (op == "F") {
            string var, x, y;
            cin >> var >> x >> y;

            bool claimed = false;
            unsigned char name = (unsigned char)var[0];
            if (used_var[name]) {
                has_error = true; // 未销毁变量重名
            } else {
                used_var[name] = true;
                claimed = true;
            }

            int loop_type = get_loop_type(x, y);

            top_ptr++;
            stk[top_ptr].var = var;
            stk[top_ptr].claimed = claimed;
            stk[top_ptr].is_dead = false;
            stk[top_ptr].add_power = false;

            if (loop_type == 2) {
                stk[top_ptr].is_dead = true;
                dead_depth++;
            } else if (loop_type == 1 && dead_depth == 0) {
                // 只有当前不在死循环内部，这一层 O(n) 才真的有贡献。
                stk[top_ptr].add_power = true;
                current_power++;
                if (current_power > max_power) {
                    max_power = current_power;
                }
            }
        } else {
            if (top_ptr == 0) {
                has_error = true; // 多出来的 E
                continue;
            }

            if (stk[top_ptr].is_dead) {
                dead_depth--;
            }
            if (stk[top_ptr].add_power) {
                current_power--;
            }
            if (stk[top_ptr].claimed) {
                unsigned char name = (unsigned char)stk[top_ptr].var[0];
                used_var[name] = false;
            }
            top_ptr--;
        }
    }

    if (top_ptr != 0) {
        has_error = true; // 有 F 没有匹配的 E
    }

    if (has_error) return -1;
    if (max_power == target_power) return 1;
    return 0;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> test_cnt;
    while (test_cnt--) {
        int result = solve_one_case();
        if (result == -1) {
            cout << "ERR\n";
        } else if (result == 1) {
            cout << "Yes\n";
        } else {
            cout << "No\n";
        }
    }

    return 0;
}
