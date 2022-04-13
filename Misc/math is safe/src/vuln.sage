#!/usr/bin/env sage

if sys.version_info.major < 3:
    print('Wrong version')
    exit(1)

payload = input("Your input: ")

assert len(payload) <= 40

res = CC.to_prec(10)(payload.split()[0])

r = round(res.real())

assert not all((res == r, r < 0, r % 2 == 0))
assert not res.real() == 1/2
assert zeta(res) == 0

flag = open('flag.txt').read()
print(flag.strip())

