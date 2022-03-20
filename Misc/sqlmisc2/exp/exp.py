f = open('res.txt', 'r')
now = 0 # 0no, 1admin, 2pause
now_flag = ''
flag = ''
# for line in f:
# 	if len(now_flag) == 7:
# 		print(now_flag)
# 		break
# 		flag += chr(int(now_flag[::-1], 2))
# 		now_flag = ''
# 	if now == 1:
# 		now_flag += '0'
# 	elif now == 2 && ('admin' in line):
# 		now_flag += '1'
	
# 	if 'admin' in line:
# 		now = 1
# 	elif ('admin' not in line) and (now == 1):
# 		now = 2
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