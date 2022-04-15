from waffleweb.request import Request

import re
import socket
import ipaddress

class WaffleProject():
    def __init__(self, apps: list):
        self.apps = apps

    def handleRequest(self, request):
        '''Handles the HTTP request.'''
        return b"HTTP/1.1 200 OK\n\nHello World"

    def run(self, host, port=80):
        #Checks if host is valid
        try:
            ipaddress.ip_address(host)
        except ValueError:
            raise ValueError('host is invalid!')

        #Checks if port is valid
        try:
            port = int(port)
            if 1 > port or port > 65535:
                raise ValueError('port is invalid!')
        except:
            raise ValueError('port is invalid!')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen(1)
            while True:
                conn, addr = sock.accept()
                req = Request(conn.recv(1024).decode(), addr)
                response = self.handleRequest(req)
                conn.sendall(response)
                conn.close()