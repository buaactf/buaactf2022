import random

def gen_func(c, idx):
    res = f'void func_{idx}(char* a1)' + '{\n'
    
    n = ord(c)
    res += "\t__asm__ __volatile__ (\n"
    res += '\t\t"lea rbx, [rip + 7]\\n\\t"\n'
    tmp = ['\t\t"inc ebx\\n\\t"\n' for _ in range(n // 4)] + ['\t\t"dec ebx\\n\\t"\n' for _ in range(n // 4)] + ['\t\t"nop\\n\\t"\n' for _ in range(n % 4)]
    random.shuffle(tmp)
    res += ''.join(tmp)
    # res += '\t\t"inc ebx\\n\\t"\n\t\t"dec ebx\\n\\t"\n' * (n // 4) + '\t\t"nop\\n\\t"\n' * (n % 4)
    res += '\t\t"lea rax, [rip + 0]\\n\\t"\n'
    res += f'\t\t"sub rax, rbx\\n\\t"\n'
    res += '\t\t"cmp al, byte ptr [rdi]\\n\\t"\n'
    res += f'\t\t"je END_{idx}\\n\\t"\n'
    res += '\t\t"push 0x3c\\n\\t"\n'
    res += '\t\t"pop rax\\n\\t"\n'
    res += '\t\t"syscall\\n\\t"\n'
    res += f'\t\t"END_{idx}:\\n\\t"\n'
    res += "\t);\n"
    if len(flag) - idx != 1:
        res += f'\tfunc_{idx+1}(a1 + 1);\n'
    res += '\treturn;\n}\n\n'
    return res

fp = open('src.c', 'w')
head = '#include <stdio.h>\n#include <stdlib.h>\nchar flag[127];\n\n'
flag = 'flag{this_is_a_test_flag}'

fp.write(head)
for i in range(len(flag)):
    fp.write(f'void func_{i}(char* a1);\n')

main = '''
int main(){
    asm(".intel_syntax noprefix\\n");
    scanf("%100s", flag);
    func_0(flag);
    printf("The flag is %s", flag);
    return 0;
}

'''
fp.write(main)

check_func = []

for i, f in enumerate(flag):
    check_func.append(gen_func(f, i))

random.shuffle(check_func)
for c in check_func:
    fp.write(c)