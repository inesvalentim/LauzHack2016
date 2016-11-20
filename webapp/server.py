#!/usr/bin/env python3

import sys
import http.server


# We will have to provide some way to forbid index... but let's forget that for now
server_address = ("", 3615)

server = http.server.HTTPServer
requestHandler = http.server.CGIHTTPRequestHandler

requestHandler.cgi_directories = ["/app"]

httpd_srv = server(server_address, requestHandler)
httpd_srv.serve_forever()
