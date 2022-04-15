import re
import socket
import ipaddress

class WaffleProject():
    def __init__(self, apps: list):
        self.apps = apps

    def handleRequest(self, request):
        '''Handles the HTTP request.'''

    def run(self, ip, port):
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            raise ValueError('ip is invalid!')

        try:
            port = int(port)
            if 1 > port or port > 65535:
                raise ValueError('port is invalid!')
        except:
            raise ValueError('port is invalid!')

        