## 考点

auto re

## 工具

反汇编/反编译工具，自动化脚本

## 步骤

逆向，然后写脚本

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

## 总结

一个对于 auto re 的尝试，可玩性很高

题目尚未完成，需要想办法避免人手暴力破解
