## 考点

椭圆曲线，pohlig_hellman攻击

## 工具

sage

## 步骤

事实上，本题的椭圆曲线是通过这种方式生成的：

```python
small_prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293]
a = 2
b = 3
def gen_special_p():
    while True:
        p = random_prime(2^200-1,False,2^199)
        E = EllipticCurve(GF(p), [a,b])
        cnt = 0
        order = E.order()
        for prime in small_prime:
            if order % prime == 0:
                cnt += 1
        if cnt >= 5:
            break
    print(p, order, factor(order))
    return p
gen_special_p()
```

可以看到椭圆曲线的阶有许多小因子，类似于素数域下基于弱素数的离散对数问题，可以采用`pohlig_hellman`攻击。

但是需要主要的是本题的阶分解后有一个特别大的因子，用这个因子去子群里跑`discrete_log`不现实，注意到密钥长度小于62位，（但是不太能用bsgs硬跑，因为电脑顶不住那么长时间，除非用什么超算吧）前几个因子计算出的结果计算中国剩余定理已经到达密钥的规模，故我们可以舍去该因子，直接用crt合并即可。

`exp.sage`:

```python
import hashlib
from Crypto.Cipher import AES

p = 1227746669897024584176049601139983199725970765368150228682221
a = 2
b = 3
E = EllipticCurve(GF(p), [a,b])
n = E.order()
G = E.gens()[0]
QA = E(302815835537564389018621724598932443372058309945965909258476, 101620440267876945129965564956309591452288432027338930366277)
QB = E(65110746247642118366859050011022338368545596077949479875681, 1017598375305367769482826313607595483103330800029116590734900)

factors = list(factor(n))

def pohlig_hellman(G, Q):
    m = 1
    moduli, remainders = [], []
    for i, j in factors:
        if i > 10 ** 9:
            break
        mod = i ** j
        g2 = G*(n//mod)
        q2 = Q*(n//mod)
        r = discrete_log(q2, g2, operation='+')
        remainders.append(r)
        moduli.append(mod)
        m *= mod

    r = crt(remainders, moduli)
    return r

def decrypt_flag(secret_key, ciphertext):
    sha1 = hashlib.sha1()
    sha1.update(str(secret_key).encode('ascii'))
    key = sha1.digest()[:16]
    iv = b'\x00' * 16
    enc = bytes.fromhex(ciphertext)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    flag = cipher.decrypt(enc).decode()
    return flag

skA = pohlig_hellman(G, QA)
skB = pohlig_hellman(G, QB)

secret_key = (QB * skA)[0]
ciphertext = 'da4ba62b1dbcdf0d8b3df8b4e253d7ef328c6a37a7d6569e9c2c577d683e1ba12d83828fdf2b2b390da5d05558f8dbcb0796ef874000f87486d679aa0c954a75'
print(decrypt_flag(secret_key, ciphertext))
```

## 总结

本题产生问题的本质在于：私钥位数过小以及用了自己生成的屑曲线。
