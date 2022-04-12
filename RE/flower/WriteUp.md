## 考点

auto re

compile:

```
python3 gensrc.py
gcc src.c -masm=intel -no-pie
```

## 工具

反汇编/反编译工具

自动化脚本

## 步骤

逆向，然后写脚本

### objdump

```python
import subprocess

dump = subprocess.check_output(['objdump', '-M', 'intel', '-j', '.text', '-d', 'a.out'], shell=False)
funcs = dump.split(b'\n\n')

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

for f in flag_list:
    print (chr(f), end='')
```

远程脚本

```python
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


p = remote("127.0.0.1", 12345)
rec = p.recvline().strip()
p.recvuntil(b'[+] Tell me the key: ')
p.sendline(solve(rec).encode())
# p.sendline(b'flag')
p.interactive()
```

### angr 版本

```python
from angr import *

proj = Project('./a2.out', main_opts={'base_addr': 0x400000})

start_state = proj.factory.entry_state()

simgr = proj.factory.simgr(start_state)

simgr.explore(find = 0x401182)

if simgr.found:
    solution = simgr.found[0]
    print (solution.posix.dumps(0))
else:
    print ("No res")
```

远程懒了，想办法找到 find 就行（或者 30 秒足够手动找 find 了）

## 总结

一个对于 auto re 的尝试，可玩性很高
