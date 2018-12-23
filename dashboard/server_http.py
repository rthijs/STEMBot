#!/usr/bin/env python3

import os

from aiohttp import web


class server_http():
    '''
    Simpele http server voor het dashboard. Gebruik het start_servers script om alle nodige services
    tegelijk te starten. Open dan http://localhost:8080 in een browser voor je je script op de robot
    uitvoert.
    '''

    current_file_dir = os.path.dirname(__file__)

    app = web.Application(debug=True)

    def __init__(self):
        self.app.router.add_get('/', self._index)
        self.app.router.add_get('/socket.io.js', self._socketiojs)
        self.app.router.add_get('/jquery-3.3.1.min.js', self._jqueryjs)
        self.app.router.add_get('/style.css', self._stylecss)

    def _index(self,request):
        with open(os.path.join(self.current_file_dir, "index.html")) as f:
            return web.Response(text=f.read(), content_type='text/html')

    def _socketiojs(self,request):
        with open(os.path.join(self.current_file_dir, "socket.io.js")) as f:
            return web.Response(text=f.read())

    def _jqueryjs(self,request):
        with open(os.path.join(self.current_file_dir, "jquery-3.3.1.min.js")) as f:
            return web.Response(text=f.read())

    def _stylecss(self,request):
        with open(os.path.join(self.current_file_dir, "style.css")) as f:
            return web.Response(text=f.read())

    def get_handler(self):
        return self.app.make_handler()