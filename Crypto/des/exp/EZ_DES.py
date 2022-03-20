#########################################################################
# Get roundKey
#########################################################################
# get the move number
def getMoveNum():
    res = [0] * 16
    for i in range(16):
        if i == 0 or i == 1 or i == 8 or i == 15:
            res[i] = 1
        else:
            res[i] = 2
    return res

# get the PC_1 table and PC_2 table
def getPC():
    PC_1_str = open('./src/PC_1.txt', 'r').read().split()
    PC_2_str = open('./src/PC_2.txt', 'r').read().split()
    PC_1 = [0] * len(PC_1_str)
    PC_2 = [0] * len(PC_2_str)
    for i in range(len(PC_1_str)):
        PC_1[i] = int(PC_1_str[i])
    for i in range(len(PC_2_str)):
        PC_2[i] = int(PC_2_str[i])
    return PC_1, PC_2

# cyclic shift to the left
def leftRow(arr, n):
    temp = [0] * n
    length = len(arr)
    for i in range(n):
        temp[i] = arr[i]
    for i in range(length):
        if i < length - n:
            arr[i] = arr[i + n]
        else:
            arr[i] = temp[i - length + n]
    return arr

# get the k0 - k16
def genKey(key):
    C = [0] * 28
    D = [0] * 28
    K = [0] * 56
    roundKey = [[0]*48 for i in range(16)]
    PC_1, PC_2 = getPC()
    moveNum = getMoveNum()
    # get K+
    for i in range(56):
        K[i] = key[PC_1[i] - 1]
    # get C0 and D0
    for i in range(28):
        C[i] = K[i]
        D[i] = K[i + 28]
    # get roundKey
    for i in range(16):
        C = leftRow(C, moveNum[i])
        D = leftRow(D, moveNum[i])
        for j in range(48):
            if PC_2[j] <= 28:
                roundKey[i][j] = C[PC_2[j] - 1]
            else:
                roundKey[i][j] = D[PC_2[j] - 28 -1]
    return roundKey
#########################################################################
# Encrypt and Decrypt
#########################################################################
#get the IP and PC_1 table
def getIP():
    IP_str = open('./src/IP.txt', 'r').read().split()
    IP_1_str = open('./src/IP_1.txt', 'r').read().split()
    IP = [0] * len(IP_str)
    IP_1 = [0] * len(IP_1_str)
    for i in range(len(IP_str)):
        IP[i] = int(IP_str[i])
    for i in range(len(IP_1_str)):
        IP_1[i] = int(IP_1_str[i])
    return IP, IP_1

# l1 xor l2
def xor(l1, l2):
    res = [0] * len(l1)
    for i in range(len(l1)):
        res[i] = l1[i] ^ l2[i]
    return res

# get the Extend table
def getE():
    E_str = open('./src/extend.txt', 'r').read().split()
    E = [0] * len(E_str)
    for i in range(len(E_str)):
        E[i] = int(E_str[i])
    return E

# extend R from 32 bit to 48 bit
def extend(R):
    res = [0] * 48
    E = getE()
    for i in range(48):
        res[i] = R[E[i] - 1]
    return res

# get sbox in 3 dim
def getSbox():
    S_str = open('./src/sbox.txt', 'r').read().split()
    S = [[[0]*16 for i in range(4)]for i in range(8)]
    l = 0
    for i in range(8):
        for j in range(4):
            for k in range(16):
                S[i][j][k] = int(S_str[l])
                l += 1
    return S

# number in dec to number in bit
def d2b(n):
    res = ''
    while n > 0:
        res += chr(n % 2 + ord('0'))
        n = n // 2
    while len(res) < 4:
        res += '0'
    return res[::-1]

# sbox replacement
def sbox(ipt):
    S = getSbox()
    res = [0] * 32
    i, l = 0, 0
    while i < 48:
        j = ipt[i] * 2 + ipt[i + 5]
        k = ipt[i + 1] * 8 + ipt[i + 2] * 4 + ipt[i + 3] * 2 + ipt[i + 4]
        temp = d2b(S[l][j][k])
        for m in range(4):
            res[m + l * 4] = int(temp[m])
        l += 1
        i += 6
    return res

# get Pbox
def getPbox():
    P_str = open('./src/pbox.txt', 'r').read().split()
    P = [0] * len(P_str)
    for i in range(len(P_str)):
        P[i] = int(P_str[i])
    return P

# pbox replacement
def pbox(ipt):
    P = getPbox()
    res = [0] * 32
    for i in range(32):
        res[i] = ipt[P[i] - 1]
    return res

# f function
def f(R, K):
    # extend R
    E_R = extend(R)
    # E_R xor K
    afterADD = xor(E_R, K)
    # sbox
    afterSbox = sbox(afterADD)
    # linear displacement
    res = pbox(afterSbox)
    return res

# Encrypt function
def DES_Encrypt(plaintext, roundkey):
    M_IP = [0] * 64
    cipher = [0] * 64
    afterF = [0] * 64
    L = [[0] * 32 for i in range(17)]
    R = [[0] * 32 for i in range(17)]
    IP, IP_1 = getIP()
    # get IP replace
    for i in range(64):
        M_IP[i] = plaintext[IP[i] - 1]
    # get L0 and R0
    for i in range(32):
        L[0][i] = M_IP[i]
        R[0][i] = M_IP[i + 32]
    for i in range(1,17):
        # L[i] = R[i - 1]
        for j in range(32):
            L[i][j] = R[i - 1][j]
        R[i] = xor(L[i - 1], f(R[i - 1], roundkey[i - 1]))
    # merge the R and L
    for i in range(64):
        if i < 32:
            afterF[i] = R[16][i]
        else:
            afterF[i] = L[16][i - 32]
    # using IP_1 replace to get cipher
    for i in range(64):
        cipher[i] = afterF[IP_1[i] - 1]
    return cipher

#########################################################################
# Main
#########################################################################
# number in hex to number in bin
def hex_to_bin(a):
    b = int(a, 16)
    res = ''
    while b > 0:
        res += chr(b % 2 + ord('0'))
        b = b // 2
    while len(res) < 4:
        res += '0'
    return res[::-1]

# text in hex to text in bin
def h2b(s):
    res = []
    for i in s:
        temp = hex_to_bin(i)
        for j in range(4):
            res.append(int(temp[j]))
    return res

# number in bin to number in hex
def bin_to_hex(a):
    b = int(a, 2)
    return hex(b)[2:]

# text in bin to text in hex
def b2h(s):
    res = ''
    now_bin = ''
    for i in range(len(s)):
        now_bin += chr(s[i] + ord('0'))
        if len(now_bin) % 4 == 0:
            res += bin_to_hex(now_bin)
            now_bin = ''
    return res


def gen_P_1():
	p = getPbox()
	p_1 = [0] * 32;
	for i in range(32):
		p_1[p[i] - 1] = i
	return p_1

def str2martix(s):
	m = [0] * 6
	for i in range(6):
		m[i] = int(s[i],  2)
	return m

def solve(plaintext, cipher):
    m = h2b(plaintext)
    c = h2b(cipher)
    C_IP = [0] * 64
    M_IP = [0] * 64
    cipher = [0] * 64
    may_after_xor = [[''for i in range(4)]for j in range(8)]
    L = [[0] * 32 for i in range(17)]
    R = [[0] * 32 for i in range(17)]
    ast = [0] * 32
    IP, IP_1 = getIP()
    before_p = [0] * 32
    S = getSbox()
    p_1 = gen_P_1()
    # get IP replace
    for i in range(64):
        M_IP[i] = m[IP[i] - 1]
        C_IP[i] = c[IP[i] - 1]
    # get L0 and R0
    for i in range(32):
        L[0][i] = M_IP[i]
        R[0][i] = M_IP[i + 32]
    for i in range(32):
    	L[1][i] = C_IP[i]
    	R[1][i] = C_IP[i + 32]
    e = extend(R[0])
    cip = xor(R[1], L[0])
    for i in range(32):
    	before_p[i] = cip[p_1[i]]
    # 还原进入sbox前的值
    for i in range(8):
    	for j in range(4):
    		for k in range(16):
    			if S[i][j][k] == int(b2h(before_p[i*4:(i+1)*4]), 16):
    				may_after_xor[i][j] = (bin(j)[2:].zfill(2)[0] + bin(k)[2:].zfill(4) + bin(j)[2:].zfill(2)[1])
    may_res = [[[]for i in range(4)]for j in range(8)]
    for i in range(8):
    	for j in range(4):
    		may_after_xor[i][j] = str2martix(may_after_xor[i][j])
    # 还原所有可能的K
    for i in range(8):
    	for j in range(4):
    		may_res[i][j] = (xor(may_after_xor[i][j], e[i*6:(i+1)*6]))
    return may_res

def gen_PC_1():
    PC_1, PC_2 = getPC()
    PC1, PC2 = [-1] * 64, [-1] * 56
    for i in range(56):
    	PC1[PC_1[i] - 1] = i
    for i in range(48):
    	PC2[PC_2[i] - 1] = i
    return PC1, PC2

# def resolve_key(roundKey):
#     C = [0] * 28
#     D = [0] * 28
#     K = [0] * 56
#     PC_1, PC_2 = getPC()
#     PC1, PC2 = gen_PC_1()
#     moveNum = getMoveNum()
#     for i in range(48):
#         if PC2[j] <= 28:
#             C[PC2[j]] = roundKey[i]
#         else:
#             D[PC2[j] - 28] = roundKey[i]
#     C = leftRow(C, 28 - moveNum[i])
#     D = leftRow(D, 28 - moveNum[i])
#     for i in range(28):
#         K[i] = C[i]
#         K[i + 28] = D[i]
#     for i in range(56):
#         key[PC1[i]] = K[i]
#     return key

if __name__ == '__main__':
    plaintext1 = "0123456789abcdef"
    plaintext2 = "fedcba9876543210"
    plaintext3 = "abcdef0123456789"
    plaintext4 = "9876543210fedcba"
    plaintext5 = "abcdefabcdefabcd"
    miwen1 = "2a138211ec75e47d"
    miwen2 = "f74ed54cb9001180"
    miwen3 = "dd465f0a99001bc4"
    miwen4 = "ee310a9baa7f46f5"
    miwen5 = "d5ec5f7f4c5f7d64"
    K1 = solve(plaintext1, miwen1)
    K2 = solve(plaintext2, miwen2)
    K3 = solve(plaintext3, miwen3)
    K4 = solve(plaintext4, miwen4)
    K5 = solve(plaintext5, miwen5)
    K = []
    for i in range(8):
    	for j in range(4):
    		if (K1[i][j] in K2[i]) and (K1[i][j] in K3[i]) and (K1[i][j] in K4[i]) and (K1[i][j] in K5[i]):
    			print(i, j)
    			K += K1[i][j]
    print(K)
    # print(resolve_key(K))