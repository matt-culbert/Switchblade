#!/usr/bin/env python3

import http.server as SimpleHTTPServer
import socketserver as SocketServer
import logging
import ssl
import sys
import asyncio

PORT = 8000
test = {}

class GetHandler(
        SimpleHTTPServer.SimpleHTTPRequestHandler
        ):

    def do_GET(self):
        temp = self.headers # Grab the headers
        temp = str(temp) # Make them a string
        temp = temp.splitlines() # Split it into a list
        temp = str(temp[-2]) # Get the last item which is the ID and make it a string(stringception)
        if 'ID' in temp: # Here we can do actions based on the ID returned
            print(temp)
        self.send_response(200)
        self.send_header("Test Dictionary Value", test) # Here we can make a custom response, perhaps pull a command from a queue
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # Gets the size of data
        post_data = self.rfile.read(content_length) # Gets the data itself

        print(post_data)

        test['ID'] = post_data # Add the ID given to us by the beacon to the dict - this should be replaced with a persistent mechanism, something like rabbidmq

async def wssServer(websocket, path):
        async def wssServer(websocket, path):
                name = await websocket.recv()
                print("< {}".format(name))

        
if sys.argv[1] == 1: # Route based on header auth
        Handler = GetHandler
        httpd = SocketServer.TCPServer(("localhost", PORT), Handler)
        httpd.serve_forever()

if sys.argv[1] == 2: # Use mTLS auth
        start_server = websockets.serve(wssServer, 'localhost', 8010)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
