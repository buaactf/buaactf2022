package main

import (
	"github.com/gin-contrib/sessions"
	"github.com/gin-contrib/sessions/cookie"
	"github.com/gin-gonic/gin"
)

func main() {
	gin.SetMode(gin.ReleaseMode)
	r := gin.Default()

	storage := cookie.NewStore(randomChar(16))
	r.Use(sessions.Sessions("o", storage))

	r.LoadHTMLGlob("template/*")

	r.GET("/login", loginGetHandler)
	r.POST("/login", loginPostHandler)

	r.GET("/secret", adminRequired(), flag)

	r.GET("/", func(c *gin.Context) { c.Redirect(302, "/login") })
	r.Run("0.0.0.0:80")
}
