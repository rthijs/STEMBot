#!/usr/bin/env python3

'''
Ik heb alles gepikt van: https://realpython.com/python-sockets/

Deze server ontvangt de berichten van de robot via een socket (IP protocol) en verstuurt socket io berichten
naar de socket io server waar ook de dashboard client applicatie mee verbindt.
'''

import socket, selectors, types
from socketIO_client import SocketIO

HOST = '10.42.0.1'  # Standard loopback interface address (localhost)
PORT = 2444        # Port to listen on (non-privileged ports are > 1023)

socketIO = SocketIO('localhost', 8081)

def send_socket_io_data(data):
    socketIO.emit('test', str(data.decode()))

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = None
        try:
            recv_data = sock.recv(1024)  # Should be ready to read
        except ConnectionResetError:
            print('Connection reset, robot stopped executing.')
        if recv_data:
            data.outb += recv_data
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            #print('echoing', repr(data.outb), 'to', data.addr)
            print(repr(data.outb))
            send_socket_io_data(data.outb)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

sel = selectors.DefaultSelector()
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST, PORT))
lsock.listen()
print('listening on', (HOST, PORT))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)