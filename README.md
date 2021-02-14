# ssm
Simple Screen Mirror 💻✨✨✨🖥️  
![screen-mirroring-icon](https://user-images.githubusercontent.com/31606119/107869470-d246af00-6ed1-11eb-8f95-acf910f27dc4.png)

## How to run
### 1. Install ssm package
- ```pip install ssm-python```

### 2. Create server.py & client.py
- sample codes [here](https://github.com/JHLeeeMe/ssm/tree/master/samples)
```python
server:
    from ssm import ScreenMirrorServer


    # ssm_server = ScreenMirrorServer(['<client-ip>', port=7890])
    ssm_server = ScreenMirrorServer()  # default: all ip & 7890 port

    ssm_server.start()



client:
    from ssm import ScreenMirrorClient


    ssm_client = ScreenMirrorClient('<server-ip>'[, port=7890, quality=90, cursor=True])

    ssm_client.start()

```

### 3. Run
1. ***server:*** ```python server.py```

2. ***client:*** ```python client.py```

### 4. Stop
- ***server:*** ```press ESC```

- ***client:*** ```kill process```
