from wsocket import WSoServ, WSoClient
import websockets
import asyncio
import time
import json

def channel_serv_1(data):
    print('server channel_1: ', data)

def channel_cli_1(data):
    print('client 1 channel_1: ', data)

def channel_cli_2(data):
    print('client 2 channel_1: ', data)

def broadcast(data):
    print('Broadcast: ', data)

serv = WSoServ(url='127.0.0.1', port=8766)
serv.add_channel('channel_1', channel_serv_1)
serv.start()

cli = WSoClient(url='127.0.0.1', port=8766, broadcast=broadcast, channel={'channel_1': channel_cli_1})
cli.connect()

time.sleep(3)

cli.send('channel_1', "This is a message !")
cli.send('channel_1', {"conf": "This is a test"})

cli2 = WSoClient(url='127.0.0.1', port=8766, broadcast=broadcast)
cli2.add_channel('channel_1', channel_cli_2)
cli2.connect()

time.sleep(3)

serv.send('channel_1', json.dumps({"key": "value"}))
serv.send('channel_1', {"key": "value"})

time.sleep(3)

serv.send('', {"all": "test"})
serv.send('channel_1', "This is a message from server to channel_1")
