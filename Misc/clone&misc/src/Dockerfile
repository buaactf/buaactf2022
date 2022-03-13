# Running locally:
# 1) echo 'flag{FLAG}' > flag.txt
# 2) docker build -t clone_misc_docker .
# 3) docker run -p 7904:1024 --rm --cap-add=SYS_ADMIN --security-opt apparmor=unconfined -it clone_misc_docker

FROM ubuntu:latest
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' > /etc/timezone
RUN sed -i s@/archive.ubuntu.com/@/mirrors.tencentyun.com/@g /etc/apt/sources.list
RUN apt-get clean
RUN apt-get update
RUN apt-get install -y sagemath
RUN sage --version

RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd /sbin/

COPY vuln.sage flag.txt /home/ctf/

USER ctf
# creates vuln.sage.py
RUN sage --nodotsage -preparse ./vuln.sage

USER root

# sane defaults
RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd

RUN chmod 555 vuln.sage && \
    chmod 555 vuln.sage.py && \
    chmod 444 flag.txt

# check whitelist of writable files/folders
RUN find / -ignore_readdir_race -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -delete
USER ctf
RUN (find --version && id --version && sed --version && grep --version) > /dev/null

USER root

EXPOSE 1024
CMD ynetd -u ctf -lt 10 -t 60 -lm 4294967296 -sh y "HOME=/home/ctf sage --nodotsage -python /home/ctf/vuln.sage.py"