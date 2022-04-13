## 考点

日志审计

sql注入

## 工具

Python

## 步骤

先url解码一下，然后往后翻找到提取flag的地方，大概在270多行，把后续的流量摘出来分析一下，发现就是一串很呆的sql语句嵌套，把逻辑缕清就能很简单的写出解密

```python
f = open('res.txt', 'r')
now = 0 # 0no, 1admin, 2pause
now_flag = ''
flag = ''
line = f.readline()
while line:
	if len(now_flag) == 7:
		flag += chr(int(now_flag[::-1], 2))
		now_flag = ''
	next_line = f.readline()
	if ('admin' in line) and ('admin' not in next_line):
		now_flag += '1'
		line = f.readline()
	elif ('admin' in line) and ('admin' in next_line):
		now_flag += '0'
		line = next_line
	elif ('admin' not in line) and ('admin' in next_line):
		line = next_line
		continue
	elif ('admin' not in line) and ('admin' not in next_line):
		line = f.readline()
		continue
print(flag)
print(len(flag))
```



## 总结

出的时候自己工具没搭好，用脚本生成的流量.....不过基础思想没啥变化
