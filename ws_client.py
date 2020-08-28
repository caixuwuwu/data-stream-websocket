#!/usr/bin/env python
# coding=utf-8

import asyncio
import json
import websockets

from helpers.kafka import producer_send
from helpers.logger import generate_logger
from settings import WS_CLIENT_HOST, WS_CLIENT_PORT, KAFKA_TOPIC_OVER_TIME_ORDER, OVER_TIME_UPPER_LIMIT, KAFKA_PARTITION_OVER_TIME_ORDER

logger = generate_logger('ws_client')


async def comsumer(message):
    try:
        message = json.loads(message)
        if 'data' in message:
            # logger.info(message['data'])
            data = message['data']
            if 'default_service_type' in data and data['default_service_type'] == 2:
                if 'in24hrs' in data:
                    over_time_area = {}
                    for area in data['in24hrs']:
                        for item in area['sub_areas']:
                            logger.debug("area_id={}, \
                                        waiting_order_long_time_top3={}, \
                                        before_pickup_order_long_time_top3={}, \
                                        delivering_order_long_time_top3={}"
                                        .format(item['area_id'],
                                                item['waiting_order_long_time_top3'],
                                                item['before_pickup_order_long_time_top3'],
                                                item['delivering_order_long_time_top3']))
                            over_time_list = list(filter(lambda x: x > OVER_TIME_UPPER_LIMIT, item['waiting_order_long_time_top3'] +
                                                    item['before_pickup_order_long_time_top3']+item['delivering_order_long_time_top3']))
                            if over_time_list:
                                over_time_area[item['area_id']] = over_time_list
                    logger.info(
                        "over_time_area.keys={}".format(over_time_area))
                    if over_time_area:
                        over_time_order = list(over_time_area.keys())
                        logger.info("over_time_order={}".format(over_time_order))
                        if over_time_order:
                            producer_send(KAFKA_TOPIC_OVER_TIME_ORDER, list(over_time_order))
    except ValueError as e:
        logger.info("message={}".format(message))
        logger.warn("message decode error. {}".format(e))


async def ws_client():
    ws_uri = "{}:{}".format(WS_CLIENT_HOST, WS_CLIENT_PORT)
    async with websockets.connect(ws_uri) as websocket:
        recv_msg = await websocket.recv()
        try:
            recv = json.loads(recv_msg)
        except ValueError as e:
            logger.warn('register fail. {}'.format(e))

        if recv is not None and recv['error'] == 0:
            async for message in websocket:
                await comsumer(message)
        else:
            logger.error('register fail. error is not zero.')

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(ws_client())
