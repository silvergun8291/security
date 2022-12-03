FROM node@sha256:1452acb56cf7d330a7c965382f81fd28b8250f1e54171d34a7c83c2794be903f

RUN apt update -y
RUN apt install cron libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon-x11-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libwayland-client0 -y

RUN echo "cce2022{REDACTED}" > /flag.txt
RUN chown root:root /flag.txt
RUN chmod 444 /flag.txt

# NOTE: app should be decompressed before docker build
ADD app /app
WORKDIR /app

RUN chown -R root:node /app
RUN chmod -R 770 /app

USER node
RUN npm install

USER root
RUN chmod -R 750 /app

ARG PORT
ENV PORT $PORT
EXPOSE $PORT

ARG SECRET
ENV SECRET $SECRET

ARG ARCHIVE_DIR
ENV ARCHIVE_DIR $ARCHIVE_DIR
RUN mkdir $ARCHIVE_DIR
RUN chown -R root:node $ARCHIVE_DIR
RUN chmod -R 770 $ARCHIVE_DIR

RUN echo "*/10 * * * * root rm -rf $ARCHIVE_DIR/*" > /etc/cron.d/blue_archive_cronjob
RUN chown root:root /etc/cron.d/blue_archive_cronjob
RUN chmod 755 /etc/cron.d/blue_archive_cronjob
RUN crontab /etc/cron.d/blue_archive_cronjob

ARG ARCHIVE_EXT
ENV ARCHIVE_EXT $ARCHlIVE_EXT

ADD entrypoint.sh /entrypoint.sh
RUN chown root:root /entrypoint.sh
RUN chmod 750 /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
