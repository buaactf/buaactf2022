from hashlib import md5
import socketserver
import random
import os
import string
import signal
# from secret import flag
flag = b'flag{practice}'

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
    
    def proof_of_work(self):
        random.seed(os.urandom(8))
        proof = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(20)])
        # print (proof)
        _hexdigits = md5(proof.encode()).hexdigest()
        self.send(f"[+] md5(XXXX+{proof[4:]}) == {_hexdigits}".encode())
        x = self.recv(prompt=b'[+] Plz tell me XXXX: ')
        if len(x) != 4 or md5(x + proof[4:].encode()).hexdigest() != _hexdigits:
            return False
        return True
    
    def handle(self):
        signal.alarm(1000)
        if not self.proof_of_work():
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
    HOST, PORT = '127.0.0.1', 23335
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()

