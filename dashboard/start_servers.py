#!/usr/bin/env python3

import threading, asyncio

from server_http import server_http

def run_server(handler, port):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = loop.create_server(handler, host='127.0.0.1', port=port)
    loop.run_until_complete(server)
    loop.run_forever()

http_handler = server_http().get_handler()

t_http = threading.Thread(target=run_server, args=(http_handler,8080))
t_http.start()




'''
import asyncio
import threading
from aiohttp import web
from server_http import server_http


def aiohttp_server():
    def say_hello(request):
        return web.Response(text='Hello, world')

    app = web.Application(debug=True)
    app.add_routes([web.get('/', say_hello)])
    handler = app.make_handler()
    return handler


def run_server(handler):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = loop.create_server(handler, host='127.0.0.1', port=8089)
    loop.run_until_complete(server)
    loop.run_forever()


t = threading.Thread(target=run_server, args=(aiohttp_server(),))
t.start()
'''