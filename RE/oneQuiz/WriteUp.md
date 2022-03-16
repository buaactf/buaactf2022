## 考点

安卓逆向，AES

## 工具

JEB pro (安卓逆向工具)

cyberchef (AES 求解工具)

## 步骤

一道安卓逆向题，打开软件后直接要输入flag：

反编译后找到`FirstActivity`，加密过程很明显，是AES/ECB加密：

用 cyberchef 可以直接解得 flag。

所以最终flag为`flag{s1mP13_L4yer_0f_J4va}`

## 总结

因为正好刚开始学安卓，心血来潮边学边出了一道安卓逆向，能力所限出得很简单