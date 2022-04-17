from http.client import responses

import waffleweb.defaults

class ResponseHeaders(dict):
    pass

class HTTPResponseBase():
    '''Handles the HTTP responses only.'''

class HttpResponse(HTTPResponseBase):
    '''Handles the HTTP responses and content.'''

    def __init__(self, content=b'', *args, **kwargs):
        pass