## 考点

block cipher 入门

## 工具

Python

## 步骤

把加密步骤捋清楚，写解密就行

S盒和P盒都可以直接逆置换整出来

```python
from libnum import n2s
s_1 = [0xc, 0xa, 0xe, 0xd, 0x1, 0xf, 0xb, 0x0, 0x7, 0x2, 0x5, 0x4, 0x3, 0x6, 0x9, 0x8]
PL_1 = [4, 0, 5, 1, 2, 7, 3, 6]
PR_1 = [3, 4, 0, 7, 6, 2, 5, 1]

def leftrow(x, num):
	left = x >> 32
	right = x & 0xffffffff
	l = ((left << num) ^ (left >> 32 - num)) & 0xffffffff
	r = ((right << num) ^ (right >> 32 - num)) & 0xffffffff
	return (l << 32) ^ r

def PL_Reverse(y):
	z = []
	for i in range(8):
		z.append((y >> (7 - i) * 8) & 0xff)
	res = 0
	for i in range(8):
		res ^= (z[PL_1[i]] << (7 - i) * 8)
	return res

def PR_Reverse(y):
	z = []
	for i in range(8):
		z.append((y >> (7 - i) * 8) & 0xff)
	res = 0
	for i in range(8):
		res ^= (z[PR_1[i]] << (7 - i) * 8)
	return res

def S_1(y, bit):
	after_sbox = 0
	for i in range(bit):
		after_sbox ^= (s_1[(y >> i * 4) & 0xf] << i * 4)
	return after_sbox

def decrypt(Y, X):
	Y0, Y1 = Y >> 64, Y & 0xffffffffffffffff
	Y0 = PL_Reverse(Y0)
	Y1 = PR_Reverse(Y1)
	Y0 = (Y0 ^ Y1) & 0xffffffffffffffff
	Y1 = (Y1 ^ leftrow(Y0, 20)) & 0xffffffffffffffff
	Y0 = (Y0 ^ leftrow(Y1, 8)) & 0xffffffffffffffff
	Y1 = (Y1 ^ leftrow(Y0, 8)) & 0xffffffffffffffff
	Y0 = (Y0 ^ leftrow(Y1, 4)) & 0xffffffffffffffff
	Y1 = (Y1 ^ Y0) & 0xffffffffffffffff
	Y0 = S_1(Y0, 128 // 8)
	Y1 = S_1(Y1, 128 // 8)
	K = X ^ ((Y0 << 64) ^ Y1)
	return K

plaintext = 0x0123456789abcdeffedcba9876543210
ciphertext1 = 0x16c95bd05e564b89e980dbf517d0f7c4
ciphertext2 = 0xe4d1e2ccf953490de0e894b47efead9c
flag1 = decrypt(ciphertext1, plaintext)
flag2 = decrypt(ciphertext2, plaintext)
print(n2s(flag1) + n2s(flag2))
```

## 总结

其实出完之后发现好像没用到啥block cipher的知识.....不过其实就是个简化了的一轮ublock，感觉可以直接把16轮写出来让大家写解密算法，好像有点过于简单了，有兴趣可以去看看ublock~
