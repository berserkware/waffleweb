class Request():
    def __init__(self, request, clientIP):
        self.headers = {}
        self.clientIP = clientIP
        self._request = request

        for line in request.split('/n'):
                splitLine = line.split(' ')
                self.headers[str(line[0][:len(line)-1])] = ' '.join(line[1:])

    @property
    def path(self):
        return self._request.split()[1]

    @property
    def method(self):
        return self._request.split()[0]