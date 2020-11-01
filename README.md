<h1 align=center>wSocket</h1>
<p align=center>Websocket communication with multiple channel</p>
<p align=center>
  <a target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-3.X-green.svg"></a>
  <a target="_blank" href="LICENSE" title="License: MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
  <a target="_blank" href="https://websockets.readthedocs.io/en/stable/" title="Require: websocket"><img src="https://img.shields.io/badge/websockets-8.1-success.svg"></a>
  <a target="_blank" href="https://docs.python.org/3/library/asyncio.html" title="Require: asyncio"><img src="https://img.shields.io/badge/asyncio-3.4.3-yellowgreen.svg"></a>
</p>

<p align="center">
  <a href="#installation">Installation</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#development">Development</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#contributing">Contributing</a>
</p>

<h3 title="installation">Installation</h3>

```console
# clone the repo
$ git clone https://github.com/LegallGuillaume/wSocket.git

# change the working directory to wSocket
$ cd wSocket

# install the module
$ python3 setup.py install
```

<h3 title="development">Development</h3>

```python
import wSocket
import time

def channel_serv_0(data):
  pass
  
def channel_cli_1(data):
  pass

def broadcast_fn(data):
  pass

serv = wSocket.WSoServ(url='127.0.0.1', port=8766, path="/socket", channel={'channel_0': channel_serv_0})
serv.start()

cli = wSocket.WSoClient(url='127.0.0.1', port=8766, path="/socket", broadcast=broadcast_fn, channel={'channel_1': channel_cli_1})
cli.connect()

time.sleep(2)
serv.send('channel_1', {"key", "value"})
serv.send('channel_1', "This is a message")

time.sleep(2)

cli.send('channel_0', "This is a answer!")

time.sleep(2)

cli.close()
serv.close()
```


<h3 title="contributing">Contributing</h3>
Please make pull request

<h3 title="author">Author(s)</h3>

* **Guillaume Le Gall** - *Initial work* - [LegallGuillaume](https://github.com/LegallGuillaume)
