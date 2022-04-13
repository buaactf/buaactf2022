import hashlib
from Crypto.Cipher import AES
# from secret import flag
flag = b'flag{M33t~you~Aga|n!!g3n3r@Te_y0vr_0Wn_Curv3_1s_5o_$4n9erours!!}'

p = 1227746669897024584176049601139983199725970765368150228682221 
a = 2
b = 3
E = EllipticCurve(GF(p), [a,b])
G = E.gens()[0]

def gen_key():
    sk = randint(1, 2 ** 62) 
    pk = G * sk
    return sk, pk

def gen_shared_secret(Q, n):
    return (Q * n)[0]

def encrypt_flag(shared_secret):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    iv = b'\x00' * 16
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(flag).hex()

def decrypt_flag(secret_key, ciphertext):
    sha1 = hashlib.sha1()
    sha1.update(str(secret_key).encode('ascii'))
    key = sha1.digest()[:16]
    iv = b'\x00' * 16
    enc = bytes.fromhex(ciphertext)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    flag = cipher.decrypt(enc).decode()
    return flag


alice_key = gen_key()
bob_key = gen_key()
print('Alice Public Key:', alice_key[1])
# Alice Public Key: (302815835537564389018621724598932443372058309945965909258476 : 101620440267876945129965564956309591452288432027338930366277 : 1)
print('Bob Public Key:', bob_key[1])
# Bob Public Key: (65110746247642118366859050011022338368545596077949479875681 : 1017598375305367769482826313607595483103330800029116590734900 : 1)
shared_secret = gen_shared_secret(alice_key[1], bob_key[0])
ciphertext = encrypt_flag(shared_secret)
print(ciphertext)
# da4ba62b1dbcdf0d8b3df8b4e253d7ef328c6a37a7d6569e9c2c577d683e1ba12d83828fdf2b2b390da5d05558f8dbcb0796ef874000f87486d679aa0c954a75