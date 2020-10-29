import websockets
from wsocket.wsthread import WSThread


class WSoServ:
    def __init__(self, **kwargs):
        self._wth = WSThread(**kwargs)
        self._flag_running = False

    def start_server(self):
        self._wth.start()
        self._flag_running = True

    def stop_server(self):
        self._wth.close_server()
        self._flag_running = False

    def send(self, channel, data) -> bool:
        if not self._flag_running:
            return False
        self._wth.send(channel, data)
        return True

    def broadcast(self, data) -> bool:
        if not self._flag_running:
            return False
        self._wth.send('', data)
        return True
    
    def add_channel(self, channel, fnptr):
        self._wth.add_channel(channel, fnptr)
