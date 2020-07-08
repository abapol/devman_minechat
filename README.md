# Minechat from devman tasks

The script listen secret minechat and save it to history file.


## How to install

For the script to work, you need Python version 3.7 and higter.

```bash
pip install -r requirements.txt
```


## How to start

```bash
python3 listen-minechat.py
```

The server will start on port 5000, host default: minechat.dvmn.org.


## Arguments

You can use this arguments:

--host : For connect to your host (default: minechat.dvmn.org)

--port : For use your port (default: 5000)

--history : To set path to file for writing chat history


Example:

```bash
python3 listen-minechat.py --host 192.168.0.1 --port 5001 --history ~/minechat.history
```
