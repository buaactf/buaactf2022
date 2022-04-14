import subprocess
from pwn import *
import base64
import tempfile
import os

context.log_level='debug'

def solve(recv):
    content = base64.b64decode(recv)
    fd, path = tempfile.mkstemp()
    with open(path, 'wb') as fp:
        fp.write(content)
    dump = subprocess.check_output(['objdump', '-M', 'intel', '-j', '.text', '-d', path], shell=False)
    funcs = dump.split(b'\n\n')
    os.remove(path)
    func_list = []
    flag_list = []
    for f in funcs:
        tmp = f.split(b'>:')
        tmp = tmp[0].split(b' <')
        if b'func' in tmp[-1]:
            func_list.append([tmp[-1], f])

    for f in func_list:
        pos = int(f[0].split(b'_')[1])
        code = f[1]
        lea = []
        for c in code.split(b'\n'):
            if b'lea ' in c:
                lea.append(c.split(b'# ')[-1].split(b' <')[0])
        res = int(lea[1], 16) - int(lea[0], 16)
        for i in range(pos - len(flag_list) + 1):
            flag_list.append(0)
        flag_list[pos] = res
    return ''.join([chr(f) for f in flag_list])


p = remote("101.43.185.64", 12345)
rec = p.recvline().strip()
p.recvuntil(b'[+] Tell me the key: ')
p.sendline(solve(rec).encode())
# p.sendline(b'flag')
p.interactive()
