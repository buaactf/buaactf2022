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
