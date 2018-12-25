#!/usr/bin/env python3

import os

os.system("python3 ./dashboard/server_http.py &")
os.system("python3 ./dashboard/server_socketio.py &")
os.system("python3 ./dashboard/server_socket.py &")
