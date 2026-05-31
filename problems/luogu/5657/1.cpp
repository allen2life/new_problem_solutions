#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

using std::cin;
using std::cout;

std::size_t n,k;
__int128 n1,k1;
int a[100];//存答案
int main (int argc, char *argv[]) {
    std::cin >> n >> k;
    n1 = n;
    k1 = k;
    for(int i =1; i<=n;i++) {
        __int128 t = 1;
        t <<= i;
        __int128 t2 = k1 / t;
        __int128 t3 = k1 % t;
        if( t2 & 1) { //奇数
            if( t3 < t/2 )
                a[i] = 1;
            else
                a[i] = 0;
        }
        else  //偶数
        {
            if( t3 < t/2 )
                a[i] = 0;
            else
                a[i] = 1;
        }
    }

    for(int i = 1;i <= n ;++i ) // i: 1->n
    {
        cout << a[n-i+1];
    }
    return 0;
}
