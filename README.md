# ssm
Simple Screen Mirroring

## How to run
### 1. Install ssm package
```bash
pip install ssm-python
```
### 2. Create server.py  
2-1. sample server code [here](https://github.com/JHLeeeMe/ssm/tree/master/samples/server.py)
```python
# in server

import threading

from ssm import ScreenMirrorServer


# ssm_server = ScreenMirrorServer(['<client-ip>', port=7890])
ssm_server = ScreenMirrorServer()  # default: all ip & 7890 port

t = threading.Thread(target=ssm_server.start)
t.start()
t.join()
```

2-2. sample client code [here](https://github.com/JHLeeeMe/ssm/tree/master/samples/client.py)
```python
# in client

import threading

from ssm import ScreenMirrorClient


ssm_client = ScreenMirrorClient('<server-ip>'[, port=7890, quality=90, cursor=True])

t = threading.Thread(target=ssm_client.start)
t.start()
```

### 3. Run server.py & client.py
```bash
# in server
python server.py

# in client
python client.py
```

### 4. Stop
```
server: 
    press ESC
    
client: 
    kill process
```
