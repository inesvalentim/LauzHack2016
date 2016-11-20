#!/usr/bin/env python3

import sys
import http.server
import os

# We will have to provide some way to forbid index... but let's forget that for now
server_address = ("", 3615)

server = http.server.HTTPServer
requestHandler = http.server.CGIHTTPRequestHandler

requestHandler.cgi_directories = ["/app"]

httpd_srv = server(server_address, requestHandler)

os.system("xdg-open http://127.0.0.1:3615/")
print("Go to http://127.0.0.1:3615/ now...")
httpd_srv.serve_forever()
