FROM ubuntu:22.04

RUN apt update
RUN apt install -y xinetd wget python3
ENV TERM=linux

RUN useradd ctf
RUN mkdir /home/ctf
COPY ./share/* /home/ctf/
COPY ./xinetd /etc/xinetd.d/ctf
EXPOSE 5333

CMD ["/usr/sbin/xinetd","-dontfork"]
