class Request():
    def __init__(self, request, clientIp):
        self.headers = request.split('\n')
        self.clientIp = clientIp

    @property
    def path(self):
        return self.headers[0].split()[1]

    @property
    def method(self):
        return self.headers[0].split()[0]

    @property
    def host(self):
        return self.headers[1].split()[1]

    @property
    def userAgent(self):
        return self.headers[2].split()[1:]

    @property
    def accept(self):
        return self.headers[3].split()[1:]

    @property
    def acceptLangauge(self):
        return self.headers[4].split()[1:]

    @property
    def acceptEncoding(self):
        return self.headers[5].split()[1:]

    @property
    def connection(self):
        return self.headers[6].split()[1]

    @property
    def cookie(self):
        return self.headers[7].split()[1:]

    @property
    def upgradeInsecureRequests(self):
        return self.headers[8].split()[1]

    @property
    def secFetchDest(self):
        return self.headers[9].split()[1]
    
    @property
    def secFetchMode(self):
        return self.headers[10].split()[1]

    @property
    def secFetchSite(self):
        return self.headers[11].split()[1]

    @property
    def secFetchUser(self):
        return self.headers[12].split()[1]

