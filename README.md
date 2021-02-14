# ssm
Simple Screen Mirror 💻✨✨✨🖥️  
![screen_mirroring_icon](https://user-images.githubusercontent.com/31606119/107869470-d246af00-6ed1-11eb-8f95-acf910f27dc4.png)

## How to run
### 1. Install ssm package
- ```pip install ssm-python```

### 2. Create server.py  
- sample codes [here](https://github.com/JHLeeeMe/ssm/tree/master/samples)
```python
server:
    import threading

    from ssm import ScreenMirrorServer


    # ssm_server = ScreenMirrorServer(['<client-ip>', port=7890])
    ssm_server = ScreenMirrorServer()  # default: all ip & 7890 port

    t = threading.Thread(target=ssm_server.start)
    t.start()
    t.join()


client:
    import threading

    from ssm import ScreenMirrorClient


    ssm_client = ScreenMirrorClient('<server-ip>'[, port=7890, quality=90, cursor=True])

    t = threading.Thread(target=ssm_client.start)
    t.start()
```

### 3. Run
1. ***server:*** ```python server.py```

2. ***client:*** ```python client.py```

### 4. Stop
- ***server:*** ```press ESC```

- ***client:*** ```kill process```
