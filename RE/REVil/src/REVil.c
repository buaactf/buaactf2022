#include <stdio.h>
#include <string.h>

#define AND  1
#define OR   2
#define NOT  3
#define XOR  4
#define ADD  5
#define SUB  6
#define SHL  7
#define SHR  8
#define MOV  9
#define MOVD 10
#define RET  11

//void add

//void sub

char vm_code[100] = {9, 3, 1, 3, 3, 1, 3, 0, 3, 0, 1, 0, 1, 2, 0, 3, 9, 1, 0, 7, 0, 2, 10, 3, 8, 6, 3, 2, 8, 1, 3, 2, 0, 1, 6, 0, 2, 11 };
int LEN_VMCODE = 90;

/*
 * ((p ^ k) <<< i) - i
 * mov eax, p
 * mov ebx, k
 * mov ecx, i
 * mov R4, 8
 *   ; xor eax, ebx
 * mov edx, ebx
 * neg edx
 * and edx, eax
 * neg eax
 * and eax, ebx
 * or eax, edx
 *
 * mov ebx, eax
 * shl eax, ecx
 * mov edx, R4
 * sub edx, ecx
 * shr ebx, edx
 * or eax, ebx
 * sub eax, ecx
 * ret eax
 */

unsigned char calc(unsigned char p, unsigned char k, unsigned char pos) {
    int i = 0;
    unsigned char R[5];
    R[0] = p;
    R[1] = k;
    R[2] = pos;
    int arg0, arg1;
    while (i < LEN_VMCODE) {
        arg0 = vm_code[i + 1];
        arg1 = vm_code[i + 2];
        switch (vm_code[i] & 0xf) {
        case AND:
            R[arg0] &= R[arg1];
            // printf("[+] R[%d] &= R[%d], R[%d] = %x\n", arg0, arg1, arg0, R[arg0]);
            i += 2;
            break;
        case OR:
            R[arg0] |= R[arg1];
            // printf("[+] R[%d] |= R[%d], R[%d] = %x\n", arg0, arg1, arg0, R[arg0]);
            i += 2;
            break;
        case NOT:
            R[arg0] = ~R[arg0];
            // printf("[+] R[%d] = ~R[%d], R[%d] = %x\n", arg0, arg0, arg0, R[arg0]);
            i += 1;
            break;
        case XOR:
            R[arg0] ^= R[arg1];
            // printf("[+] R[%d] ^= R[%d], R[%d] = %x\n", arg0, arg1, arg0, R[arg0]);
            i += 2;
            break;
        case ADD:
            R[arg0] += R[arg1];
            // printf("[+] R[%d] += R[%d], R[%d] = %x\n", arg0, arg1, arg0, R[arg0]);
            i += 2;
            break;
        case SUB:
            R[arg0] -= R[arg1];
            // printf("[+] R[%d] -= R[%d], R[%d] = %x\n", arg0, arg1, arg0, R[arg0]);
            i += 2;
            break;
        case SHL:
            R[arg0] <<= R[arg1];
            // printf("[+] R[%d] <<= R[%d], R[%d] = %x\n", arg0, arg1, arg0, R[arg0]);
            i += 2;
            break;
        case SHR:
            R[arg0] >>= R[arg1];
            // printf("[+] R[%d] >>= R[%d], R[%d] = %x\n", arg0, arg1, arg0, R[arg0]);
            i += 2;
            break;
        case MOV:
            R[arg0] = R[arg1];
            // printf("[+] R[%d] = R[%d], R[%d] = %x\n", arg0, arg1, arg0, R[arg0]);
            i += 2;
            break;
        case MOVD:
            R[arg0] = arg1;
            // printf("[+] R[%d] = %d, R[%d] = %x\n", arg0, arg1, arg0, R[arg0]);
            i += 2;
            break;
        case RET:
            // printf("[+] ret R[0]\n");
            return R[0];
        default:
            printf("Wrong opcode!");
            exit(1);
        }
        i += 1;
    }
    return 0;
}

void decrypt(char* a, int len, char* k) {
    for (int i = 0; i < len; i++) {
        a[i] = calc(a[i], k[i % 8], i % 8);
    }
    return;
}

int main() {
    //printf("%02X", calc(0x58, 0x20, 1));
    //return 0;
    
    char key[100];
    printf("Send me 300RMB of bitcoins to get the key\nInput the Key: ");
    scanf("%10s", key);
    FILE* fid;
    fid = fopen("flag.png.enc", "rb");
    if (fid == NULL) {
        printf("Can't find encrypt file");
        return 1;
    }
    fseek(fid, 0, SEEK_END);
    int num = ftell(fid);
    rewind(fid);
    char* pos = (char*)malloc(sizeof(char) * num);
    if (pos == NULL) {
        printf("Error occurred");
        return 1;
    }
    fread(pos, sizeof(char), num, fid);
    fclose(fid);
    decrypt(pos, num, key, strlen(key));
    fid = fopen("flag.png", "rb");
    fwrite(pos, sizeof(char), num, fid);
    fclose(fid);
    free(pos);
    pos = 0;
    return 0;
}

