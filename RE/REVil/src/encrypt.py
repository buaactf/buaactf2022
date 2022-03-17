def ror(x, k):
    return (x >> k) | (x << (8 - k)) & 0xff

def encrypt(x, k):
    res = b''
    for i, c in enumerate(x):
        c += i
        c &= 0xff
        c = ror(c, i)
        c ^= k[i % len(k)]
        res += c.to_bytes(1, 'little')
    return res

# In [30]: random.seed(s2n(b'Generate_key_for_RE_challenge_REVil'))

# In [31]: ''.join(random.choices(string.printable[:94], k=8))
# Out[31]: '<^uG|veR'

key = b'<^uG|veR'
plain = open('flag.png', 'rb').read()
# plain = b'abcdefg'
cipher = b''
for i in range(0, (len(plain) + 7), 8):
    cipher += encrypt(plain[i: i + 8], key)
# print (cipher)
open('flag.png.enc', 'wb').write(cipher)
