### 考点

python_socket 自动化脚本编写+md5碰撞

### 工具

python（废话），`fast_coll`md5碰撞工具

### 步骤

##### 第一问

问题本身没啥好说的，主要就是脚本的编写。

其实也比较简单，使用socket库，建立tcp连接，调用recv、send进行交互就行了。注意通过合理的sleep和recv字节数设置等 让recv收到想要的东西（例如，一次性把前面的题目介绍全收完，而不是漏了一句而导致后面出错） 

```python
import socket
from time import sleep
from gmpy2 import invert
address=('121.37.201.92',10001)
client=socket.socket()
client.connect(address)
sleep(1)
data=client.recv(10240)
print("server reply:",data)
client.send(b'2')
for i in range(300):
    data=str(client.recv(512))
    print(data)
    a=m=0
    j=2
    while(data[j]!=' '):
        a=a*10+int(data[j])
        j+=1
    j+=1
    while(data[j]!='\\'):
        m=m*10+int(data[j])
        j+=1
    print((invert(a,m)))
    client.send(str(invert(a,m)).encode())
    sleep(2)

data = str(client.recv(512))
print(data)
client.close()
```

##### 第二问

在网上寻找md5碰撞相关内容，可以找到fastcoll工具。（也可以找到当年王小云院士关于md5碰撞的论文，但CTF题有现成工具肯定用现成的，就不管它了。）

其实本题 nc 套接字 是可以直接与终端交互的，但是生成的hex碰撞文件（字符串）往往编码不出人话，所以用脚本提交是最稳妥的

```python
import socket
from time import sleep
address=('121.37.201.92',10001)
client=socket.socket()
client.connect(address)
sleep(1)
data=client.recv(1024)
print(data)
client.send(b'3')
sleep(1)
r1=open("1.txt","rb")
r2=open("2.txt","rb")
x=r1.read()
y=r2.read()
r1.close()
r2.close()
client.send(x)
sleep(2)
client.send(y)
sleep(2)
data=client.recv(1024)
print(data)
client.close()
```

两个文件是用fastcoll生成的md5值相同的文件。

### **总结**

本题比较简单，主要考察大家脚本编写能力和信息搜集能力，同时增添一点比赛的乐趣（交互题还是比较好玩的）

### flag

`BUAACTF{Cr3pT0_Is_60_1nte2esTin3!}`