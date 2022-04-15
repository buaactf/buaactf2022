#include<stdio.h>
#include<stdlib.h>

// gcc -fno-stack-protector -no-pie -z now -o easyrop easyrop.c

long long R00T[0x200] = {0};


int main(int argc, char const *argv[])
{
    alarm(30);
    R00T[0x50] = &alarm;
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    char buf[0x40];
    read(0, buf, 0x100);
    return 0;
}