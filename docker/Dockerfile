FROM python:3.6-slim

ADD docker/sources_mirrors_163.list /etc/apt/sources.list

RUN set -xe && apt-get update \
    && apt-get install -y --allow-unauthenticated libssl-dev default-libmysqlclient-dev make g++ git libgomp1 \
    && pip install -U pip && pip install --no-cache-dir websockets pytz sqlalchemy redis requests ujson arrow mysqlclient aliyun-log-python-sdk kafka-python\
    && apt-get purge -y --auto-remove libssl-dev make g++ git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /data/websocket/

ADD . /data/websocket/

CMD ["python", "ws_server.py"]