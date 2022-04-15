from libnum import n2s, s2n
from random import randrange
from Crypto.Util.Padding import pad
from Crypto.Util.number import *

flag = pad(b'BUAACTF{******************}', 48)

def gen():
    e = 3
    while True:
        try:
            p = getPrime(512)
            q = getPrime(512)
            n = p*q
            phi = (p-1)*(q-1)
            d = inverse(e,phi)
            if d == 1:
                continue
            return p,q,d,n,e
        except:
            continue
    return
p,q,d,n,e = gen()
c = pow(s2n(flag), e, n)
print("n = %d"%n)
print("e = %d"%e)
print("c = %d"%c)
print("mbar = %d"%(s2n(flag[:len(flag) // 2]) << 192))

# n = 81990486158830819987073862172415164961593278461441199000999472465202518599850332550812125141470698747706547832071653895197966292731285323989845213159146261837803561813706450672725878328449137240949801181034766354744732582372151328001276074276010039350214840101550595192803830418941509645225250637084951191901
# e = 3
# c = 29567745406946076830146052374930033424211480116321544674448562777091588294881623860014915348606939136520110465290092616212926800744828796888106944346222024613999754846412634549763305673101149427233979469362411909357450400895307369148973536710380608978693814012874175410588472106640257194122351943446376090522
# mbar = 10209587263099434303402268295264783241039304732220412954880929680985232124926643894842588590120872193397691703623680