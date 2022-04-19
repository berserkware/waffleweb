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






