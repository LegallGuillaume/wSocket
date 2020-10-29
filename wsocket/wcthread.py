import threading
import asyncio
import websockets
import json

class WCThread(threading.Thread):
    def __init__(self, **kwargs):
        self.port = kwargs.pop('port', 8765)
        thread_name = kwargs.pop('thread_name', f'wsoclient-{self.port}')
        self._loop = kwargs.pop('loop', asyncio.new_event_loop())
        self.url = kwargs.pop('url', '127.0.0.1')
        self.path = kwargs.pop('path', '/')
        self.broadcast_fn = kwargs.pop('broadcast', self._broadcast)
        if self.path.startswith('/'):
            self.path = self.path[1:]

        if kwargs:
            raise Exception('Argument error ', kwargs)
        threading.Thread.__init__(self, name=thread_name)
        self._channel = {}

    def run(self):
        self._cli = None
        self._loop.run_until_complete(self._recv_from_serv())

    def add_channel(self, channel, fnptr):
        self._channel[channel] = fnptr

    def send(self, channel, data):
        if not self._cli:
            return
        if isinstance(data, str):
            data = json.dumps({"message": data.replace('\'', "'")})
        try:
            msg = json.dumps({channel: data})
            coro = self._cli.send(msg)
            asyncio.run_coroutine_threadsafe(coro, self._loop)
        except websockets.exceptions.ConnectionClosed:
            pass

    async def _recv_from_serv(self):
        async with websockets.client.connect("ws://{}:{}/{}".format(self.url, str(self.port), self.path), loop=self._loop) as client:
            self._cli = client
            while True:
                try:
                    message = await self._cli.recv()
                    jrowdata = json.loads(message)
                    for channel, data in jrowdata.items():
                        if channel in self._channel:
                            self._channel[channel](data)
                        elif channel == '':
                            self.broadcast_fn(data)
                except websockets.exceptions.ConnectionClosed:
                    pass

    def _broadcast(self, data):
        pass