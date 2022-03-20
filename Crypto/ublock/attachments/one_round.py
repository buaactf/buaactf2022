######################
# ublock for 128/128 #
######################

######################
# default_parameter  #
######################

s = [0x7, 0x4, 0x9, 0xc, 0xb, 0xa, 0xd, 0x8, 0xf, 0xe, 0x1, 0x6, 0x0, 0x3, 0x2, 0x5]
s_1 = [0xc, 0xa, 0xe, 0xd, 0x1, 0xf, 0xb, 0x0, 0x7, 0x2, 0x5, 0x4, 0x3, 0x6, 0x9, 0x8]
PL1 = [1, 3, 4, 6, 0, 2, 7, 5]
PL_1 = [4, 0, 5, 1, 2, 7, 3, 6]
PR1 = [2, 7, 5, 0, 1, 6, 4, 3]
PR_1 = [3, 4, 0, 7, 6, 2, 5, 1]
PK1 = [6, 0, 8, 13, 1, 15, 5, 10, 4, 9, 12, 2, 11, 3, 7, 14]
RC = [0x988cc9dd, 0xf0e4a1b5, 0x21357064, 0x8397d2c6, 0xc7d39682, 0x4f5b1e0a, 0x5e4a0f1b, 0x7c682d39, 0x392d687c, 0xb3a7e2f6, 0xa7b3f6e2, 0x8e9adfcb, 0xdcc88d99, 0x786c293d, 0x30246175, 0xa1b5f0e4, 0x8296d3c7, 0xc5d19480, 0x4a5e1b0f, 0x55410410, 0x6b7f3a2e, 0x17034652, 0xeffbbeaa, 0x1f0b4e5a]

################
# Key_Generate #
################

def PK(x):
	z = []
	for i in range(16):
		z.append((x >> (15 - i) * 4) & 0xf)
	res = 0
	for i in range(16):
		res ^= (z[PK1[i]] << (15 - i) * 4)
	return res >> 32, res & 0xffffffff

def Mod2Multi(a):
	return ((a << 1) ^ 19) if ((a << 1) >= 16) else (a << 1)

def T(K):
	z = []
	for i in range(8):
		z.append((K >> i * 4) & 0xf)
	res = 0
	for i in range(8):
		res ^= Mod2Multi(z[i]) << i * 4
	return res

def keygen(K):
	rk = []
	rk.append(K)
	for i in range(16):
		K0, K1, K2, K3 = K >> 96, (K >> 64) & 0xffffffff, (K >> 32) & 0xffffffff, K & 0xffffffff
		K0, K1 = PK((K0 << 32) ^ K1)
		K2 = K2 ^ S(K0 ^ RC[i], 128 // 16)
		K3 = K3 ^ T(K1)
		K = (K2 << 96) ^ (K3 << 64) ^ (K1 << 32) ^ K0
		rk.append(K)
	return rk

##############
# Encryption #
##############

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

def encrypt(x, rk):
	x0, x1 = x >> 64, x & 0xffffffffffffffff
	rk0, rk1 = rk[0] >> 64, rk[0] & 0xffffffffffffffff
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
##############
# Decryption #
##############

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

def decrypt(Y, rk):
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
	X = rk[0] ^ ((Y0 << 64) ^ Y1)
	return X

if __name__ == '__main__':
	x = 0x0123456789abcdeffedcba9876543210
	key1 = 0x425541414354467b64305f7930755f6b
	key2 = 0x6e30775f7468335f75626c30636b3f7d
	cipher1 = encrypt(x, key1)
	cipher2 = encrypt(x, key2)
	print(hex(cipher1))
	print(hex(cipher2))