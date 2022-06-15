FROM python:3.9

COPY . /crawler
WORKDIR /crawler

RUN pip install -r requirements.txt

RUN apt update && apt install tzdata -y
ENV TZ="Asia/Seoul"

RUN apt install cron -y

COPY cron /etc/cron.d/cron

RUN chmod 0755 /etc/cron.d/cron
RUN crontab /etc/cron.d/cron
RUN touch /var/log/cron.log

EXPOSE 8082

CMD ["cron","-f"]


