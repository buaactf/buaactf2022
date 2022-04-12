# syntax=docker/dockerfile:1

FROM golang:1.16-alpine

WORKDIR /app

COPY src /app/

RUN go env -w GOPROXY=https://goproxy.cn,direct && \
    go mod download && \
    go build -o /gogetit 

CMD [ "/gogetit" ]