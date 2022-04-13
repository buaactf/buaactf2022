import socketserver
from time import sleep
from hashlib import md5
from gmpy2 import invert
from Crypto.Util.number import getPrime
from random import randint
from secret import flag

MENU = br'''[+] Let's play games!Which game would y like to play?
[+] 1. Plz find invert(a,m) when a and m is given(300 asks)
[+] 2. Plz find a pair of 'x'and'y' that satisfying x!=y && md5(x)===md5(y)
'''

class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 2048
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
                msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'[-] '):
        self.send(prompt, newline=False)
        return self._recvall()

    def handle(self):
        self.send(MENU, newline=False)
        self.send(b"[+] Plz give me your choice: ")
        ans = int(self.recv().strip().decode())
        if ans == 1:
            for i in range(300):
                a = m = 1
                while a % m == 0 or m % a == 0:
                    a = randint(2,2**8)
                    m = getPrime(6)
                self.send(("[+] Here is your (a, m): (%s, %s)" % (a, m)).encode())
                self.send(b"[+] Plz give me your answer: ")
                ans = int(self.recv().strip().decode())
                if ans != invert(a, m):
                    self.send(b'[!] oops!')
                    break
            if i == 299:
                self.send(b'[!] ' + flag[:16])

        elif ans == 2:
            self.send(b"[+] Plz give me your x: ")
            x = self.recv()
            self.send(b"[+] Plz give me your y: ")
            y = self.recv()
            if (x == y) or (md5(x).hexdigest() != md5(y).hexdigest()):
                self.send(b'[!] oops!')
            else:
                self.send(b'[!] ' + flag[16:])
        
        else:
            self.send(b'[!] oops!')
        self.request.close()

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 43089
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()