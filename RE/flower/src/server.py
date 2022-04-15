from hashlib import md5
import socketserver
import random
import os
import string
import signal
import subprocess
import base64
import tempfile

flag = b'flag{Thi5_m@Y_H3lp_y0u_Get_s7arted_1n_auto_REV}'

head = '#include <stdio.h>\n#include <stdlib.h>\nchar flag[127];\n\n'
main = '''
int main(){
    asm(".intel_syntax noprefix\\n");
    scanf("%100s", flag);
    func_0(flag);
    printf("Correct!\\n");
    return 0;
}

'''

class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 1024
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()
    
    def send(self, msg, newline=True):
        try:
            if newline:
                msg += b"\n"
            self.request.sendall(msg)
        except:
            pass
    
    def recv(self, prompt=b'[-]' ):
        self.send(prompt, newline=False)
        return self._recvall()
    
    def gen_func(self, c, idx, len_key):
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
        res += f'\t\t"je $+7\\n\\t"\n'
        res += '\t\t"push 0x3c\\n\\t"\n'
        res += '\t\t"pop rax\\n\\t"\n'
        res += '\t\t"syscall\\n\\t"\n'
        # res += f'\t\t"END_{idx}:\\n\\t"\n'
        res += "\t);\n"
        if len_key - idx != 1:
            res += f'\tfunc_{idx+1}(a1 + 1);\n'
        res += '\treturn;\n}\n\n'
        return res
    
    def gen_challenge(self):
        random.seed(os.urandom(8))
        key = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(32)])
        # print (key)
        fd, path = tempfile.mkstemp()
        try:
            with open(path, 'w') as fp:
                # do stuff with temp file
                fp.write(head)
                for i in range(len(key)):
                    fp.write(f'void func_{i}(char* a1);\n')
                fp.write(main)
                check_func = []
                for i, f in enumerate(key):
                    check_func.append(self.gen_func(f, i, len(key)))
                random.shuffle(check_func)
                for c in check_func:
                    fp.write(c)
        except:
            print (b"Errors occurred, please contact admin!")
            return False
        finally:
            res = subprocess.call(['gcc', '-x', 'c', path, '-o', path + '.out', '-masm=intel', '-no-pie'])
            if res != 0:
                self.send(b"Errors occurred, please contact admin!")
            else:
                fp = open(path+'.out', 'rb')
                output = base64.b64encode(fp.read())
                fp.close()
                self.send(output)
                x = self.recv(prompt=b'[+] Tell me the key: ').decode()
                os.remove(path)
                if x == key:
                    return True
                return False
        return False
    
    def handle(self):
        signal.alarm(30)
        if not self.gen_challenge():
            self.send(b"Wrong!")
            self.request.close()
            return
        self.send(flag)
        self.request.close()

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    HOST, PORT = '0.0.0.0', 12345
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()

