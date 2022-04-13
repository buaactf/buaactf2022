## 考点

DES一轮差分

## 工具

Python

## 步骤

按照数学推导一步步还原即可，具体推导如下
$$
有如下等式\\
L_1=R_0\\
R_1=L_0\oplus F(R_0,K_0)\\
可以做如下推导\\
F(R_0,K_0)=R_1\oplus L_0\\
可以倒推到F函数P^{-1}操作之前\\
通过S盒差分爆破出所有的可能输入\\
然后用L_1和R_0的值进行对比找到K_0即为flag
$$


```python
def solve(plaintext, cipher):
    m = h2b(plaintext)
    c = h2b(cipher)
    C_IP = [0] * 64
    M_IP = [0] * 64
    cipher = [0] * 64
    may_after_xor = [[''for i in range(4)]for j in range(8)]
    L = [[0] * 32 for i in range(17)]
    R = [[0] * 32 for i in range(17)]
    ast = [0] * 32
    IP, IP_1 = getIP()
    before_p = [0] * 32
    S = getSbox()
    p_1 = gen_P_1()
    # get IP replace
    for i in range(64):
        M_IP[i] = m[IP[i] - 1]
        C_IP[i] = c[IP[i] - 1]
    # get L0 and R0
    for i in range(32):
        L[0][i] = M_IP[i]
        R[0][i] = M_IP[i + 32]
    for i in range(32):
    	L[1][i] = C_IP[i]
    	R[1][i] = C_IP[i + 32]
    e = extend(R[0])
    cip = xor(R[1], L[0])
    for i in range(32):
    	before_p[i] = cip[p_1[i]]
    # 还原进入sbox前的值
    for i in range(8):
    	for j in range(4):
    		for k in range(16):
    			if S[i][j][k] == int(b2h(before_p[i*4:(i+1)*4]), 16):
    				may_after_xor[i][j] = (bin(j)[2:].zfill(2)[0] + bin(k)[2:].zfill(4) + bin(j)[2:].zfill(2)[1])
    may_res = [[[]for i in range(4)]for j in range(8)]
    for i in range(8):
    	for j in range(4):
    		may_after_xor[i][j] = str2martix(may_after_xor[i][j])
    # 还原所有可能的K
    for i in range(8):
    	for j in range(4):
    		may_res[i][j] = (xor(may_after_xor[i][j], e[i*6:(i+1)*6]))
    return may_res

```



## 总结

把课上讲过的(可能)DES差分从三轮简化到了一轮，原理没变化
