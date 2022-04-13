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
    C = leftRow(C, moveNum[i])
    D = leftRow(D, moveNum[i])
    for j in range(48):
        if PC_2[j] <= 28:
            roundKey[0][j] = C[PC_2[j] - 1]
        else:
            roundKey[0][j] = D[PC_2[j] - 28 -1]
    for i in range(16):
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
    for j in range(32):
        L[1][j] = R[0][j]
    R[1] = xor(L[0], f(R[0], roundkey[0]))
    for i in range(64):
        if i < 32:
            afterF[i] = L[1][i]
        else:
            afterF[i] = R[1][i - 32]
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

if __name__ == '__main__':
    flag = "*******"
    res = ''
    for i in flag:
        res += bin(ord(i))[2:].zfill(7)
    real_flag = []
    for i in res[:-1]:
        real_flag.append(int(i))
    print(real_flag)

    plaintext1 = "0123456789abcdef"
    plaintext2 = "fedcba9876543210"
    plaintext3 = "abcdef0123456789"
    plaintext4 = "9876543210fedcba"
    plaintext5 = "abcdefabcdefabcd"
    k = [real_flag]
    plt1 = h2b(plaintext1)
    plt2 = h2b(plaintext2)
    plt3 = h2b(plaintext3)
    plt4 = h2b(plaintext4)
    plt5 = h2b(plaintext5)

    ciphertext1 = DES_Encrypt(plt1, k)
    ciphertext2 = DES_Encrypt(plt2, k)
    ciphertext3 = DES_Encrypt(plt3, k)
    ciphertext4 = DES_Encrypt(plt4, k)
    ciphertext5 = DES_Encrypt(plt5, k)

    print('ciphertext1 = ' + b2h(ciphertext1))
    print('ciphertext2 = ' + b2h(ciphertext2))
    print('ciphertext3 = ' + b2h(ciphertext3))
    print('ciphertext4 = ' + b2h(ciphertext4))
    print('ciphertext5 = ' + b2h(ciphertext5))
    # ciphertext1 = 2a138211ec75e47d
    # ciphertext2 = f74ed54cb9001180
    # ciphertext3 = dd465f0a99001bc4
    # ciphertext4 = ee310a9baa7f46f5
    # ciphertext5 = d5ec5f7f4c5f7d64
