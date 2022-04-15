FROM python:3.8.8
WORKDIR /app

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
    && sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
    && apt-get update

COPY src/requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY src .

RUN echo 'flag{465fb68b-8198-4412-8764-ce5dddb85e93}' > /flag \
    && chmod 600 /flag \
    && chmod -R 755 /app \
    && useradd -m buaactf

ADD readflag.c /readflag.c
RUN apt -y install gcc && \
    gcc /readflag.c -o /readflag && \
    chmod +s /readflag && \
    rm /readflag.c

USER buaactf

EXPOSE 8080
CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]
