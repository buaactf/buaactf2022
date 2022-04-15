#include <iostream>
#include <functional>
#define mod 1000000007
// "flag{1_am_the_mast3r_0f_1ambda!}";
int dst[] = { 232158417,905829108,139226748,642534132,792302047,185163016,882244924,139226748,304372182,882244924,369890567,778495828,509087178,882244924,304372182,139226748,262605169,369890567,958626347,422530824,882244924,78457748,232158417,882244924,185163016,139226748,304372182,212410164,152452523,139226748,253860160,592383835 };
char flag[33];
int main(int argv,char **argc)
{
    std::cout << "please input the flag:" << std::endl;;
    std::cin >> flag;
    const auto y = [](const auto& f) {
        return [&f](const auto& x) {return x(x); }(
            [&f](const auto& x)->std::function<bool(int)> {
                return [&f, &x](int n) {
                    return f(x(x))(n);
                };
            });
    };
    const auto y2 = [](const auto& f) {
        return [&f](const auto& x) { return x(x); } ([&f](const auto& x)
            -> std::function<int(int)> {
                return f([&x](int n) { return x(x)(n); });
            });
    };

    auto metafact = [](auto&& fact) {
        return [fact](int n) {
            return n <1 ? 1 : (1LL*n*fact(n-1))%mod;
        };
    };
    auto metacheck = [&](auto&& check)
    {
        return [&,check](int n)
        {
            return n<0?true:y2(metafact)(1024 + flag[n]) == dst[n] ? check(n - 1) : false;
        };
    };
    bool result = y(metacheck)(31);
    if (result)
        std::cout << "right" << std::endl;
    else
        std::cout << "wrong" << std::endl;
}

