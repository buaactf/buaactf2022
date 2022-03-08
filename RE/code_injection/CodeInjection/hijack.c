#include<Windows.h>
#include<stdio.h>

#define _CRT_SECURE_NO_WARNINGS

int (*p)(const char*, ...) = 0x140001000;
int (*s)(const char*, ...) = 0x140001060;
void (*e)(int) = 0x140001BF8;

void shellcode_func (void) {
	char con1[] = { 'C','o','n','g','r','a', 0 };
	char con2[] = { 't', 'u', 'l', 'a', 't', 0 };
	char con3[] = {'i', 'o', 'n', 's', '!', 0};	//写做一整行可能会被优化到rdata段
	char fmt[] = { '%','s',0};
	char wro[] = { 'W','r', 'o','n','g','!',0};
	unsigned char res[] = { 51, 57, 52, 50, 46, 22, 58, 49, 48, 28, 59, 63, 48, 54, 33, 60, 58, 59, 28, 38, 20, 22, 58, 58, 57, 2, 52, 44, 1, 58, 29, 60, 63, 52, 54, 62, 22, 58, 49, 48, 40};	//41
//flag{CodeInjectionIsACoolWayToHijackCode}
	char input[41] = { 0 };

	s(fmt,input);
	for (int i = 0; !(input[i] ^ 0x55 ^ res[i]); i++) {
		if (i == 40) {
			p(con1);
			p(con2);
			p(con3);
			e(0);
		}
	}
	p(wro);
	e(0);
}

void smc(CONTEXT ctx) {
	STARTUPINFOA si = { 0 };
	si.cb = sizeof(si);
	PROCESS_INFORMATION pi = { 0 };
	CreateProcessA(NULL, (LPSTR)"inject_victim.exe", NULL, NULL, FALSE, NULL, NULL, NULL, &si, &pi);
	SuspendThread(pi.hThread);
	LPVOID lpBuffer = VirtualAllocEx(pi.hProcess, NULL, 0x142, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
	WriteProcessMemory(pi.hProcess, lpBuffer, shellcode_func, 0x142, NULL);
	
	ctx.ContextFlags = CONTEXT_ALL;
	GetThreadContext(pi.hThread, &ctx);
	ctx.Rip = (DWORD64)lpBuffer;
	SetThreadContext(pi.hThread, &ctx);
	ResumeThread(pi.hThread);
}


int main(){
	unsigned char* p = shellcode_func;
	CONTEXT ctx = { 0 };
	for (int i = 0; i < 0x142; i++) {
		*(p + i) = *(p + i) ^ 0x20;
	}
	smc(ctx);

	return 0;
}
