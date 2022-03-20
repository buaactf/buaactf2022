from libnum import s2n,n2s,invmod
from re import findall
from secret import letter,shifter

def move(n,k):
    s = bin(n)[2:].zfill(64)
    return int(s[k:] + s[:k], 2)

# letter = "Hello. My name is Logistic and the whole system is under my control. I'm suffering from great amnesia recently and have forgotten where and how I hide the flag. I can only remember the key I use is 8yeRp9oLH3qcc7I. Help me find my flag, please."
# shifter = [5, 51, 37, 22, 26, 52, 36, 17, 54, 38, 60, 10, 61, 8, 55, 15, 23, 13, 33, 42, 40, 19, 21, 12, 39, 43, 28, 50, 24, 47, 16]

# 加密
message = list(map(s2n,findall(r".{1,8}",letter)))
for i in range(31):
    message[i] = move(message[i],shifter[i])
p = getPrime() # 52750358975649354449407
q = getPrime() # 23574637757246841069594107658796543
e = 65537
for i in range(31):
    message[i] = pow(message[i],e,p*q)
print(message)

# 解密
d = invmod(e,(p-1)*(q-1))
for i in range(31):
    message[i] = pow(message[i],d,p*q)
for i in range(31):
    for j in range(64):
        print(n2s(move(message[i],j))) # 爆破找关键字

