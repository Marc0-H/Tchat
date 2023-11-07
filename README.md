# Tchat - A terminal chat application

Chat application in python (3.10.12) made with curses

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
