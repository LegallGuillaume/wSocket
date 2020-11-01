import threading
import asyncio
import websockets
import json

class WSThread(threading.Thread):
    def __init__(self, **kwargs):
        self.port = kwargs.pop('port', 8765)
        thread_name = kwargs.pop('thread_name', f'wsoserver-{self.port}')
        self._loop = kwargs.pop('loop', asyncio.new_event_loop())
        self.url = kwargs.pop('url', '127.0.0.1')
        self.path = kwargs.pop('path', '/')
        self.unknown_channel = kwargs.pop('unknown_channel', None)
        self._channel = kwargs.pop('channel', {})
        if not asyncio.iscoroutinefunction(self.unknown_channel):
            self.unknown_channel = None
        if self.path.startswith('/'):
            self.path = self.path[1:]

        if kwargs:
            raise Exception('Argument error ', kwargs)
        self._flag_running = False
        self._queue = asyncio.Queue(loop=self._loop)
        threading.Thread.__init__(self, name=thread_name)
        self._clients = []

    def run(self):
        self._srv = websockets.serve(self._server_loop, self.url, self.port, loop=self._loop)
        self._loop.run_until_complete(self._srv)
        self._flag_running = True
        self._loop.run_until_complete(self._loop_queue())

    def close_server(self):
        self._flag_running = False
        self._srv.close()
        super().join()

    def get_clients(self):
        return self._clients

    def send(self, channel, data):
        if isinstance(data, str):
            data = {"message": data.replace('\'', '"')}
        ndata = {channel.replace('\'', '"'): data}
        try:
            message = json.dumps(ndata)
        except json.JSONDecodeError:
            raise Exception('Error send message to client : {}'.format(data))

        coro = self._queue.put(message)
        asyncio.run_coroutine_threadsafe(coro, self._loop)

    async def _register_client(self, client):
        self._clients.append(client)

    async def _unregister_client(self, client):
        try:
            await client.close()
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self._clients.remove(client)

    async def unregister_all_client(self):
        for client in self._clients:
            try:
                await client.close()
            except websockets.exceptions.ConnectionClosed:
                continue
        self._clients.clear()

    async def _server_loop(self, websocket, origin_path):
        path = origin_path[1:]
        if self.path is not path:
            await websocket.close()
            return
        await self._register_client(websocket)
        while websocket.open:
            try:
                message = await websocket.recv()
                if message == "<QUIT>":
                    await websocket.close()
                    continue
                rowdata = json.loads(message)
                for channel, data in rowdata.items():
                    if channel in self._channel:
                        self._channel[channel](websocket, data)
                    elif self.unknown_channel:
                        self.unknown_channel(websocket, data)
            except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK):
                break
        await self._unregister_client(websocket)

    async def _send_to_clients(self, channel, data: str):
        ndata = json.dumps({channel: data})
        if channel in self._channel:
            for client in self._clients:
                try:
                    await client.send(ndata)
                except websockets.exceptions.ConnectionClosed:
                    continue
        elif channel == '':
            for client in self._clients:
                try:
                    await client.send(ndata)
                except websockets.exceptions.ConnectionClosed:
                    continue

    async def _loop_queue(self):
        while self._flag_running:
            message = await self._queue.get()
            if message is not None:
                jrow = json.loads(message)
                for channel, data in jrow.items():
                    await self._send_to_clients(channel, json.dumps(data))
            self._queue.task_done()

    def add_channel(self, channel, fn):
        self._channel[channel] = fn
