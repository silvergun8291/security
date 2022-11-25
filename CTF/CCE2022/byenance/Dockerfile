FROM ubuntu:jammy

RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -y socat

RUN useradd -d /home/byenance/ -m -p byenance -s /bin/bash byenance
WORKDIR /home/byenance
COPY byenance ./byenance
COPY flag ./flag
CMD socat TCP-LISTEN:6464,reuseaddr,fork EXEC:./byenance
