FROM ubuntu:22.04

RUN apt update
RUN apt install -y xinetd qemu-system-x86-64
ENV TERM=linux

RUN useradd ctf

CMD ["/usr/sbin/xinetd","-dontfork"]
