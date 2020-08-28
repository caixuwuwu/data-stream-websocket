#!/usr/bin/env python
# coding=utf-8

import sys

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

from helpers.logger import generate_logger
from settings import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC_OVER_TIME_ORDER

logger = generate_logger('helpers.kafka')

producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(","))


def producer_send(topic, messages, partition=None):

    def on_send_success(record_metadata):
        logger.info("record_metadata.topic={}".format(record_metadata.topic))
        logger.info("record_metadata.partition={}".format(
            record_metadata.partition))
        logger.info("record_metadata.offset={}".format(record_metadata.offset))

    def on_send_error(excp):
        logger.error('I am an errback', exc_info=excp)

    if isinstance(messages, str):
        messages = [messages]
    for msg in messages:
        producer.send(topic, msg.encode(), partition=partition).add_callback(
            on_send_success).add_errback(on_send_error)
    producer.flush()


def get_consumer(topic, group_id=None, auto_offset_reset='latest'):
    # To consume latest messages and auto-commit offsets
    consumer = KafkaConsumer(topic,
                            group_id=group_id,
                            auto_offset_reset=auto_offset_reset,
                            bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS])
    return consumer


if __name__ == "__main__":
    kafka_type = sys.argv[1]
    if kafka_type == 'producer':
        producer_send(KAFKA_TOPIC_OVER_TIME_ORDER, sys.argv[2].split(','))
    elif kafka_type == 'consumer':
        consumer = get_consumer(KAFKA_TOPIC_OVER_TIME_ORDER, auto_offset_reset='earliest')
        for message in consumer:
            # message value and key are raw bytes -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            logger.info("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                message.offset, message.key,
                                                message.value))
    else:
        print("parameter invalid!")
