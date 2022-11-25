FROM python:3.9.13@sha256:2cea326d2eb1ea18f8846f722ae7fed6064f5c9912ebe615b47e3621c33e2097

USER root

RUN apt update -y && apt install python3-pip -y
RUN /usr/bin/python3 -m pip install --upgrade pip
RUN /usr/bin/python3 -m pip install Flask gunicorn

COPY app /app
COPY build/token_ext.so /app/lib/token_ext.so

RUN useradd -d /app -s /bin/bash app
RUN chown -R root:app /app
RUN chmod -R 750 /app

RUN echo "cce2022{REDACTED}" > /flag.txt
RUN chown root:root /flag.txt
RUN chmod 444 /flag.txt

WORKDIR /app
USER app
EXPOSE 8080
CMD ["/usr/bin/python3", "/usr/local/bin/gunicorn", "-w", "8", "--bind", "0.0.0.0:8080", "wsgi:app"]
