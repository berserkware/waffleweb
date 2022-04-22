from http.client import responses

import waffleweb
import json

class HTTP404(Exception):
    pass

class ResponseHeaders(dict):
    def __init__(self, data):
        self._headers = {}

        #splits data into the seporate headers
        if data:
            for header in data.split('\n'):
                splitHeader = header.strip().split(' ')
                self[splitHeader[0][:(len(splitHeader[0]) - 1)]] = ' '.join(splitHeader[1:])

    def __setitem__(self, key, value):
        self._headers[key] = value

    def __delitem__(self, key):
        del self._headers[key]

    def __getitem__(self, key):
        return self._headers[key]

    def __contains__(self, value):
        return True if value in self._headers.keys() else False

    def items(self):
        '''Returns all headers'''
        return self._headers.items()

class HTTPResponseBase():
    '''Handles the HTTP responses only.'''
    
    statusCode = 200

    def __init__(
        self, headers=None, contentType=None, charset=None, status=None, reason=None
    ):
        self.headers = ResponseHeaders(headers)
        self._charset = charset

        #Checks if content type is in headers if it isn't adds one
        if 'Content-Type' not in self.headers:
            if contentType is None:
                contentType = f'text/html; charset={self.charset}'
            self.headers['Content-Type'] = contentType
        elif contentType:
            raise ValueError(
                'You cannot have a contentType provided if you have a Content-Type in your headers.'
            )

        #Checks if status code is valid.
        if status is not None:
            try:
                self.statusCode = int(status)
            except(ValueError, TypeError):
                raise TypeError('HTTP status code has to be an integer.')

            if 100 > status or status > 599:
                raise ValueError('HTTP status code must be a integer from 100 to 599.')
        self._reasonPhrase = reason

    @property
    def reasonPhrase(self):
        if self._reasonPhrase is not None:
            return self._reasonPhrase
        return responses.get(self.statusCode, "Unknown status code.")
        
    @reasonPhrase.setter
    def reasonPhrase(self, value):
        self._reasonPhrase = value

    @property
    def charset(self):
        '''Gets charset if charset is None, gets defualt charset.'''
        if self._charset is not None:
            return self._charset

        return waffleweb.defaults.DEFAULT_CHARSET

    @charset.setter
    def charset(self, value):
        self._charset = value        

    def serializeHeaders(self):
        '''This gets just the headers in a binary string.'''
        return b'\r\n'.join([
            key.encode(self.charset) + b': ' + value.encode(self.charset)
            for key, value in self.headers.items()
        ])

    __bytes__ = serializeHeaders    

    def convertBytes(self, value):
        '''Encodes value and converts it to bytes.'''
        if isinstance(value, str):
            return bytes(value, encoding=self.charset)

        return bytes(str(value), encoding=self.charset)

class HTTPResponse(HTTPResponseBase):
    '''Handles the HTTP responses and content.'''

    def __init__(self, content=b'', *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.content = content 

    def serialize(self):
        '''This gets the fully binary string including headers and content.'''
        return b'HTTP/1.1 ' + self.convertBytes(self.statusCode) + b' ' + self.convertBytes(self.reasonPhrase) + b'\r\n' + self.serializeHeaders() + b'\r\n\r\n' + self.content

    __bytes__ = serialize

    @property
    def content(self):
        return b"".join(self._content)

    @content.setter
    def content(self, value):
        self._content = [self.convertBytes(value)]

class JSONResponse(HTTPResponseBase):
    '''Handles the HTTP responses and json.'''

    def __init__(self, json={}, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.json = json
        self.headers['Content-Type'] = f'application/json; charset={self.charset}'

    def serialize(self):
        '''This gets the fully binary string including headers and json.'''
        return b'HTTP/1.1 ' + self.convertBytes(self.statusCode) + b' ' + self.convertBytes(self.reasonPhrase) + b'\r\n' + self.serializeHeaders() + b'\r\n\r\n' + self.json

    __bytes__ = serialize

    @property
    def json(self):
        return self._json

    @json.setter
    def json(self, value):
        self._json = bytes(json.dumps(value), encoding=self.charset)