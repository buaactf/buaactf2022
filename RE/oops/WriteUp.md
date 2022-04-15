## 考点

c++

## 工具

反汇编/反编译工具

## 步骤

看着比较乱（有符号的话更乱一点），看上去有一些像是库函数的东西，不过仔细阅读可以发现就是一个简单的求阶乘递归函数

```c++
#include <iostream>
#include <vector>
#define mod 1000000007
std::vector<int> dst = { 232158417,905829108,139226748,642534132,792302047,185163016,882244924,139226748,304372182,882244924,369890567,778495828,509087178,882244924,304372182,139226748,262605169,369890567,958626347,422530824,882244924,78457748,232158417,882244924,185163016,139226748,304372182,212410164,152452523,139226748,253860160,592383835 };
constexpr int fact(const int i) {
    return i == 0 ? 1 : (1LL * i * fact(i - 1)) % mod;
}
int main(int argv, char** argc)
{
    const long long fact1024 = fact(1024);
    auto solveOne = [fact1024](int num) -> char {
        long long factN = fact1024;
        for (int i = 0;;) {
            if (factN == num) {
                return i;
            }
            i++;
            factN = (factN*(i + 1024)) % mod;
        }
        return -1;
    };
    std::string ans;
    for (auto v : dst) {
       ans += solveOne(v);
    }
    std::cout << ans << std::endl;
}
```
