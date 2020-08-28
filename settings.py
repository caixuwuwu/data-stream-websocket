#!/usr/bin/env python
# -*- encoding:utf-8 -*-
'''
    配置項.
'''
import os

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
REDIS_DB = os.environ.get('REDIS_DB', '1')

# HBASE_HOST = os.environ['HBASE_HOST']
# HBASE_PORT = os.environ['HBASE_PORT']

WS_SERVER_HOST = os.environ.get('WS_SERVER_HOST', '0.0.0.0')
WS_SERVER_PORT = os.environ.get('WS_SERVER_PORT', '52475')
WS_CLIENT_HOST = os.environ.get('WS_CLIENT_HOST', 'ws://localhost')
WS_CLIENT_PORT = os.environ.get('WS_CLIENT_PORT', '52475')

ALIYUN_LOG_ENDPOINT = os.environ.get('ALIYUN_LOG_ENDPOINT')
ALIYUN_LOG_ACCESS_KEY_ID = os.environ.get('ALIYUN_LOG_ACCESS_KEY_ID')
ALIYUN_LOG_ACCESS_KEY = os.environ.get('ALIYUN_LOG_ACCESS_KEY')
ALIYUN_LOG_PROJECT_NAME = os.environ.get('ALIYUN_LOG_PROJECT_NAME')
ALIYUN_LOG_STORE_NAME = os.environ.get('ALIYUN_LOG_STORE_NAME')

KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_PARTITION_OVER_TIME_ORDER = int(os.environ.get('KAFKA_PARTITION_OVER_TIME_ORDER', 0))
KAFKA_TOPIC_OVER_TIME_ORDER = os.environ.get('KAFKA_TOPIC_OVER_TIME_ORDER')

#超时状态判定，单位：分钟， 默认：30分钟
OVER_TIME_UPPER_LIMIT = int(os.environ.get('OVER_TIME_UPPER_LIMIT', 30))
