FROM ubuntu:22.04

RUN apt-get update 
RUN apt-get install -y build-essential
RUN apt-get install -y libmnl0 libmnl-dev
RUN apt-get install -y libnl-3-dev libnl-genl-3-dev
RUN apt-get install -y xinetd wget

RUN useradd ctf

RUN mkdir /home/ctf
ADD share/proximity /home/ctf/proximity
ADD share/flag /flag

RUN chmod 460 /home/ctf/*
RUN chown ctf:root /home/ctf/*
RUN chmod +x /home/ctf/proximity
RUN chmod 444 /flag

ADD xinetd /etc/xinetd.d/
EXPOSE 5555
CMD ["/usr/sbin/xinetd","-dontfork"]
