import os

from urllib.parse import urlparse

from waffleweb.response import HTTP404, HTTPResponse
from waffleweb.static import StaticHandler

class Request():
    def __init__(self, requestHeaders, clientIP):
        self.headers = {}
        self.clientIP = clientIP
        self.requestHeaders = requestHeaders

        #Splits the request into it's seporate headers and adds it to a dictionary.
        splitHeaders = requestHeaders.split('\n')
        for line in splitHeaders:
                splitLine = line.strip().split(' ')
                self.headers[str(splitLine[0][:(len(splitLine[0]) - 1)])] = ' '.join(splitLine[1:])

    @property
    def path(self):
        return self.requestHeaders.split('\n')[0].split()[1]

    @property
    def method(self):
        return self.requestHeaders.split('\n')[0].split()[0]

    @property
    def HTTPVersion(self):
        return self.requestHeaders.split('\n')[0].split()[2]

    @property
    def host(self):
        return self.headers['Host']

    @property
    def userAgent(self):
        return self.headers['User-Agent']

    @property
    def accept(self):
        return self.headers['Accept']

    @property
    def acceptLanguage(self):
        return self.headers['Accept-Language']

    @property
    def acceptEncoding(self):
        return self.headers['Accept-Encoding']

    @property
    def connection(self):
        return self.headers['Connection']

    @property
    def cookie(self):
        return self.headers['Cookie']

class RequestHandler:
    def __init__(self, request, clientIP, apps):
        self.request = Request(request, clientIP)
        self.apps = apps

    def _splitURL(self) -> tuple:
        reqPath = urlparse(self.request.path).path

        #gets the root and file extenstion
        root, ext = os.path.splitext(reqPath)
        root = root.strip('/')
        splitRoot = root.split('/')

        return (root, splitRoot, ext)

    def findView(self):
        #Searches through all the apps to match the url
        for app in self.apps:
            app = app['app']
            for view in app.views:
                urlMatches = True
                viewKwargs = {}
                if view['path'] == self.root:
                    return view['view'](self.request)

                if len(view['splitPath']) == len(self.splitRoot) and view['splitPath'] != ['']:
                    for index, part in enumerate(view['splitPath']):
                        if part != self.splitRoot[index] and type(part) == str:
                            urlMatches = False
                            break
                        
                        if type(part) == list:
                            if part[1] == 'int':
                                viewKwargs[str(part[0])] = int(self.splitRoot[index])
                            elif part[1] == 'float':
                                viewKwargs[str(part[0])] = float(self.splitRoot[index])
                            else:
                                viewKwargs[str(part[0])] = str(self.splitRoot[index])

                    if urlMatches:
                        return view['view'](self.request, **viewKwargs)
        
        raise HTTP404

    def getResponse(self):
        self.root, self.splitRoot, self.ext = self._splitURL()
        if self.ext == '':
            try:
                return self.findView()
            except HTTP404:
                return HTTPResponse('The requested page could not be found', status=404)
        else:
            try:
                handler = StaticHandler(self.root, self.splitRoot, self.ext)
                return handler.findFile()
            except HTTP404:
                return HTTPResponse('The requested file could not be found', status=404)