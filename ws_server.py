#!/usr/bin/env python

# WS server example
import asyncio
import json
import websockets
import http
from helpers.logger import generate_logger
from settings import WS_SERVER_HOST, WS_SERVER_PORT
from view import view_function

LOGGER = generate_logger('ws_server')
CLIENT_SOCKS = set()
REMOVE_SOCKS = set()

def process_request(path, request_headers):
    path = path.rstrip('/')
    LOGGER.info('request path={}'.format(path))
    LOGGER.debug('request headers={}'.format(request_headers))
    if path == '/heartbeat':
        return http.HTTPStatus.OK, [], b'OK'


async def resp_dashboard(websocket):
    data = view_function()
    LOGGER.info('resp_dashboard: %s is replied.', data)
    await websocket.send(data)


async def register(websocket):
    CLIENT_SOCKS.add(websocket)
    LOGGER.info("Socket %s is added.", websocket.remote_address)
    await websocket.send(json.dumps({'error': 0}))


async def unregister(websocket):
    CLIENT_SOCKS.remove(websocket)
    LOGGER.info("Socket %s is removed.", websocket.remote_address)


async def notify_users(data):
    if CLIENT_SOCKS:
        await asyncio.wait([sock.send(data) for sock in CLIENT_SOCKS])


async def main(websocket, path):
    await register(websocket)
    try:
        async for data in websocket:
            LOGGER.info("receive data: %s", data)
            if data.lower() == 'heartbeat':
                await websocket.send(data)
                LOGGER.info('%s is replied.', data)
            else:
                data_dict = {}
                try:
                    data_dict = json.loads(data)
                except json.decoder.JSONDecodeError:
                    msg = 'received invalid json'
                    await websocket.send({
                        "error_msg": msg,
                        "error": -1
                    })
                    LOGGER.warning("{}. data={}".format(msg, data))
                if 'path' in data_dict and data_dict['path'] == '/v2/dashboard':
                    await resp_dashboard(websocket)
                elif 'error' in data_dict and data_dict['error'] == 0:
                    await notify_users(data)
                    LOGGER.info('Message %s is published.', data)
                else:
                    LOGGER.warning("no data process. %s", data)
    except websockets.exceptions.ConnectionClosed as err:
        LOGGER.info('Closed with %d, %r, %s', err.code, err.reason, websocket.remote_address)
    finally:
        await unregister(websocket)


if __name__ == '__main__':
    server = websockets.serve(main, WS_SERVER_HOST, WS_SERVER_PORT, process_request=process_request)
    LOGGER.info('start running... {}:{}'.format(WS_SERVER_HOST, WS_SERVER_PORT))
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()
