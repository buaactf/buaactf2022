#include<stdio.h>

int (*p)(const char*, ...) = printf;
int (*s)(const char*, ...) = scanf;


int main() {
	printf("Where is the flag?");
}