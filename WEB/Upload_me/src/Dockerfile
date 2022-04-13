FROM python:3.7-slim-buster
WORKDIR /opt/app

RUN sed -i "s/http:\/\/deb.debian.org/http:\/\/mirrors.ustc.edu.cn/g" /etc/apt/sources.list
RUN sed -i "s/http:\/\/security.debian.org/http:\/\/mirrors.ustc.edu.cn/g" /etc/apt/sources.list

RUN apt update -y
RUN apt install gcc zip -y

COPY src /opt/app/
ADD files/flag /flag
ADD files/readflag.c /readflag.c

RUN pip install -r /opt/app/requirements.txt --no-cache-dir &&\
    chmod 600 /flag && \
    gcc /readflag.c -o /readflag && \
    chmod +s /readflag && \
    rm /readflag.c

RUN adduser \
    --disabled-login \
    -u 1011 \
    --gecos "" \
    --shell /bin/bash \
    friday

RUN chown -R 1011:1011 /opt/app

USER 1011
EXPOSE 10008
ENTRYPOINT ["python"]
CMD ["/opt/app/app.py"]