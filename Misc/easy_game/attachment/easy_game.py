#!/usr/bin/python2

from time import sleep
from hashlib import md5
from gmpy2 import invert
from Crypto.Util.number import getPrime
from random import randint
from sys import exit

flag = 'flag{********************************}'

MENU = r'''[+] Let's play games!Which game would y like to play?
[+] 1. Plz find invert(a,m) when a and m is given(300 asks)
[+] 2. Plz find a pair of 'x'and'y' that satisfying x!=y && md5(x)===md5(y)
'''

def game():
    print(MENU)
    sleep(1)
    ans=input()

    if ans==1:
        i=0
        for i in range(300):
            a = m = 1
            while a%m==0 or m%a==0:
                a=randint(2,2**8)
                m=getPrime(6)
            print("[+] Here is your (a, m): (%s, %s)" % (a, m))
            print("[+] Plz give me your answer: ")
            ans=input()
            if int(ans)!=invert(a,m):
                print(b'0ops!')
                break
        if i==299:
            print(flag[:19])
        exit(0)

    if ans==2:
        i=0
        print("[+] Plz give me your x: ")
        x=input()
        sleep(1)
        print("[+] Plz give me your y: ")
        y=input()
        if(x==y) or (md5(x).hexdigest() != md5(y).hexdigest()):
            print(b'0ops!')
        else:
            print(flag[19:])
        sleep(10)
        exit(0)

if __name__ == "__main__":
    game()
