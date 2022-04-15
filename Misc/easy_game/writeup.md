# easy_game
## 题目描述
I made an eye-diff between crypto-ezgame and misc-easygame and I found that the flag is not in the code file, which means i need to read flag in the system. Of course, I also found a lot of differences between the two challenges. For example, i have never made a challenge with python2🧛‍♂️
## 考点
python2的```input```函数存在命令执行
## 思路
本题为密码学题目ez_game同名题目，观察发现2者实现了同一个功能。该题换为了python2编写同时没有import flag，意味着需要我们rce。
## poc
```python
__import__('os').system('/bin/sh')
```
