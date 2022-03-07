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
	unsigned char res[] = { 0, 10, 7, 1, 29, 37, 9, 2, 3, 47, 8, 12, 3, 5, 18, 15, 9, 8, 27 };	//19
//flag{CodeInjection}
	char input[19] = { 0 };

	s(fmt,input);
	for (int i = 0; !(input[i] ^ 0x66 ^ res[i]); i++) {
		if (i == 18) {
			p(con1);
			p(con2);
			p(con3);
			e(0);
		}
	}
	p(wro);
	e(0);
}

int main(){
	//shellcode_func();
	STARTUPINFOA si = { 0 };
	si.cb = sizeof(si);

	PROCESS_INFORMATION pi = {0};

	CreateProcessA(NULL, (LPSTR)"inject_victim.exe", NULL, NULL, FALSE, NULL, NULL, NULL, &si, &pi);
	SuspendThread(pi.hThread);
	LPVOID lpBuffer = VirtualAllocEx(pi.hProcess, NULL, 0x107, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
	WriteProcessMemory(pi.hProcess, lpBuffer, shellcode_func, 0x107, NULL);
	CONTEXT ctx = { 0 };
	ctx.ContextFlags = CONTEXT_ALL;
	GetThreadContext(pi.hThread, &ctx);
	ctx.Rip = (DWORD64)lpBuffer;
	SetThreadContext(pi.hThread, &ctx);
	ResumeThread(pi.hThread);
	return 0;
}
