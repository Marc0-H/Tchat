# Tchat - A terminal chat application

Chat application in python (3.10.12) in terminal made with curses

![tchat_vid-_online-video-cutter com_(1)](https://github.com/Marc0-H/Tchat/assets/79107936/96b77e03-dd31-4f57-ae59-937ed328380f)

## Installation

Once the repo has been downloaded use the following commands to install the required python libraries and run the application:

### Linux/Mac:
```
pip3 install -r requirements.txt
python3 main.py
```
### Windows:
```
pip install -r win_requirements.txt
py main.py
```

## Commands

```
/server --ip <ip_address> --port <port> --name <server_name>
/join --ip <ip_address> --port <port>
/clear
/disconnect
```

For localhost only you can just use /server and /join

## Libraries used
* socket
* select
* pickle
* threading
* curses
* math
* argparse
* datetime

## Future To-do

* Implement left arrow, right arrow, del
* Implement /help command
* Error handling
* Make sidebar look good
