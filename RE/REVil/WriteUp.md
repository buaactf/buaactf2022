## 考点

- 简单的 vm
- 根据 png 文件头获得 key

## 工具

- ida / ghidra ...
- python / c / go ...
- hexdump / 010editor ...

## 步骤

逆一下 vm

```
; ((p ^ k) <<< i) - i
mov eax, p
mov ebx, k
mov ecx, i
mov R4, 8
  ; xor eax, ebx
mov edx, ebx
neg edx
and edx, eax
neg eax
and eax, ebx
or eax, edx

mov ebx, eax
shl eax, ecx
mov edx, R4
sub edx, ecx
shr ebx, edx
or eax, ebx
sub eax, ecx
ret eax
```

png文件的文件头是固定的8字节，所以已知明密文，可以直接求 key

求出来 key: <^uG|veR

运行程序，输入key，就有 flag 了

## 总结

无
