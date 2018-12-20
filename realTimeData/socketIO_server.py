#!/usr/bin/env python3

'''
Dit is de server voor socket io berichten. Applicaties die hier gebruik van willen maken
moeten verbinden met de poort gedefineerd in de PORT variabele.
'''

import socketio
from aiohttp import web

PORT = 8081

sio = socketio.AsyncServer()
sio.__setattr__('origins', '*:*')  # prevent Cross-Origin Request Blocked error
app = web.Application()
sio.attach(app)

@sio.on('connect')
async def connect(sid, environ):
    print("connect ", sid)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('test')
async def test(sid, data):
    print(data)
    print("sending data: " + str(data))
    await sio.emit('test', str(data))
    print("klaar met zenden.")

web.run_app(app, port=8081)