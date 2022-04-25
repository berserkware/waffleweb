import os
from posixpath import split

from urllib.parse import urlparse

from waffleweb.response import HTTP404

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

    def splitURL(self) -> tuple:
        reqPath = urlparse(self.request.path).path

        #gets the root and file extenstion
        root, ext = os.path.splitext(reqPath)
        root = root.strip('/')
        splitRoot = root.split('/')

        return (root, splitRoot, ext)
    
    def getResponse(self):
        root, splitRoot, ext = self.splitURL()

        if ext == '':
            #Searches through all the apps to match the url
            for app in self.apps:
                module = app['module']
                app = app['app']

                for view in app.views:
                    urlMatches = True
                    viewKwargs = {}

                    if view['path'] == root:
                        return view['view'](self.request)

                    if len(view['splitPath']) == len(splitRoot) and view['splitPath'] != ['']:
                        for index, part in enumerate(view['splitPath']):
                            if part != splitRoot[index] and type(part) == str:
                                urlMatches = False
                                break
                            
                            if type(part) == list:
                                if part[1] == 'int':
                                    viewKwargs[str(part[0])] = int(splitRoot[index])
                                elif part[1] == 'float':
                                    viewKwargs[str(part[0])] = float(splitRoot[index])
                                else:
                                    viewKwargs[str(part[0])] = str(splitRoot[index])

                        if urlMatches:
                            return view['view'](self.request, **viewKwargs)
        else:
            pass

        #Returns 404 if doesn't match URL
        raise HTTP404