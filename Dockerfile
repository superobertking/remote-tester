FROM python:3.5.2

RUN mkdir -p /server/logs
WORKDIR /server
VOLUME /server/logs
EXPOSE 23 233 2333 23333 66 666 6666
# TODO: Use iptables to get the real ip after forwarded by docker.

COPY . /server
# CMD python3 server.py > logs/log-`date +%s%n` 2>&1
CMD python3 server.py
