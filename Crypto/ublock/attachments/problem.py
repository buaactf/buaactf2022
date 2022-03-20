from secret import flag
from libnum import s2n
s = [0x7, 0x4, 0x9, 0xc, 0xb, 0xa, 0xd, 0x8, 0xf, 0xe, 0x1, 0x6, 0x0, 0x3, 0x2, 0x5]
PL1 = [1, 3, 4, 6, 0, 2, 7, 5]
PR1 = [2, 7, 5, 0, 1, 6, 4, 3]

def leftrow(x, num):
	left = x >> 32
	right = x & 0xffffffff
	l = ((left << num) ^ (left >> 32 - num)) & 0xffffffff
	r = ((right << num) ^ (right >> 32 - num)) & 0xffffffff
	return (l << 32) ^ r

def S(x, bit):
	after_sbox = 0
	for i in range(bit):
		after_sbox ^= (s[(x >> i * 4) & 0xf] << i * 4)
	return after_sbox

def PL(x):
	z = []
	for i in range(8):
		z.append((x >> (7 - i) * 8) & 0xff)
	res = 0
	for i in range(8):
		res ^= (z[PL1[i]] << (7 - i) * 8)
	return res

def PR(x):
	z = []
	for i in range(8):
		z.append((x >> (7 - i) * 8) & 0xff)
	res = 0
	for i in range(8):
		res ^= (z[PR1[i]] << (7 - i) * 8)
	return res

def encrypt(x, K):
	x0, x1 = x >> 64, x & 0xffffffffffffffff
	rk0, rk1 = K >> 64, K & 0xffffffffffffffff
	x0 = S(x0 ^ rk0, 128 // 8)
	x1 = S(x1 ^ rk1, 128 // 8)
	x1 = (x1 ^ x0) & 0xffffffffffffffff
	x0 = (x0 ^ leftrow(x1, 4)) & 0xffffffffffffffff
	x1 = (x1 ^ leftrow(x0, 8)) & 0xffffffffffffffff
	x0 = (x0 ^ leftrow(x1, 8)) & 0xffffffffffffffff
	x1 = (x1 ^ leftrow(x0, 20)) & 0xffffffffffffffff
	x0 = (x0 ^ x1) & 0xffffffffffffffff
	x0 = PL(x0)
	x1 = PR(x1)
	Y = (x0 << 64) ^ x1
	return Y

if __name__ == '__main__':
	x = 0x0123456789abcdeffedcba9876543210
	key1, key2 = s2n(flag[:len(flag) // 2]), s2n(flag[len(flag) // 2:])
	cipher1 = encrypt(x, key1)
	cipher2 = encrypt(x, key2)
	print('plaintext =' + hex(x))
	print('ciphertext1 =' + hex(cipher1))
	print('ciphertext2 =' + hex(cipher2))

# plaintext = 0x0123456789abcdeffedcba9876543210
# ciphertext1 = 0x16c95bd05e564b89e980dbf517d0f7c4
# ciphertext2 = 0xe4d1e2ccf953490de0e894b47efead9c