package main

import (
	"fmt"
	"html/template"
	"math/rand"

	"github.com/gin-contrib/sessions"
	"github.com/gin-gonic/gin"
)

type User struct {
	User     string
	Password string
}

func randomChar(l int) []byte {
	output := make([]byte, l)
	rand.Read(output)
	return output
}

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

func loginPostHandler(c *gin.Context) {
	uname := c.PostForm("uname")
	pwd := c.PostForm("pwd")
	if uname == "admin" {
		c.String(200, "noon,you cant be admin")
		return
	}
	if uname == "" || pwd == "" {
		c.String(200, "empty parameter")
		return
	}

	s := sessions.Default(c)
	s.Set("uname", uname)
	s.Save()
	c.Redirect(302, "/secret")
}

func loginGetHandler(c *gin.Context) {
	c.HTML(200, "login", gin.H{
		"title": "Go get it",
	})
}

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
