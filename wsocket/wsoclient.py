import websockets
from wsocket.wcthread import WCThread

class WSoClient:
    def __init__(self, **kwargs):
        self._cli = WCThread(**kwargs)
        self._flag_running = False

    def connect(self):
        self._cli.start()
        self._flag_running = True

    def send(self, channel, data) -> bool:
        if not self._flag_running:
            return False
        self._cli.send(channel, data)
        return True

    def broadcast(self, data) -> bool:
        if not self._flag_running:
            return False
        self._cli.send('', data)
        return True
    
    def add_channel(self, channel, fnptr):
        self._cli.add_channel(channel, fnptr)
