import waffleweb
import json
import os
import importlib
import mimetypes
try:
    settings = importlib.import_module('settings')
except ModuleNotFoundError:
    settings = None

from datetime import datetime
from pytz import timezone
from http.client import responses

from waffleweb.cookie import Cookies, Cookie
from waffleweb.template import renderTemplate
from waffleweb.datatypes import MultiValueOneKeyDict

class HTTP404(Exception):
    pass

class HTTPResponseBase():
    '''Handles the HTTP responses only.'''
    
    statusCode = 200

    def __init__(
        self, contentType=None, charset=None, status=None, reason=None
    ):
        self.headers = MultiValueOneKeyDict({})
        self._charset = charset

        #Added content type to headers
        if contentType is None:
            contentType = f'text/html; charset={self.charset}'
        self.headers['Content-Type', None] = contentType

        #Adds date headers
        now = datetime.now(timezone('GMT'))
        dateTime = now.strftime("%a, %d %b %Y %X %Z")
        self.headers['Date', None] = dateTime

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

        if hasattr(settings, 'CHARSET'):
            return getattr(settings, 'CHARSET')
        return waffleweb.defaults.DEFAULT_CHARSET

    @charset.setter
    def charset(self, value):
        self._charset = value 

    def setCookie(
            self, 
            name, 
            value, 
            path=None, 
            maxAge=None, 
            domain=None, 
            secure=False, 
            HTTPOnly=False, 
            sameSite='Lax', 
        ):
        '''Sets a cookie to a value, takes two arguments: name and value'''
        if path is not None:
            self.headers['Set-Cookie'] = Cookie(name=name, value=value, path=path, maxAge=maxAge, domain=domain, secure=secure, HTTPOnly=HTTPOnly, sameSite=sameSite)
        elif path is None and self.request is not None:
            self.headers['Set-Cookie'] = Cookie(name=name, value=value, path=self.request.path, maxAge=maxAge, domain=domain, secure=secure, HTTPOnly=HTTPOnly, sameSite=sameSite)
        else:
            self.headers['Set-Cookie'] = Cookie(name=name, value=value, path='/', maxAge=maxAge, domain=domain, secure=secure, HTTPOnly=HTTPOnly, sameSite=sameSite)  

    def deleteCookie(self, name):
        '''Deletes a cookie if exists, takes one argument: name.'''
        if 'Set-Cookie' in self.headers.keys():
            if type(self.headers['Set-Cookie']) == list:
                for count, cookie in enumerate(self.headers['Set-Cookie']):
                    if cookie.name == name:
                        del self.header['Set-Cookie'][count]
            else:
                if self.headers['Set-Cookie'].name == name:
                    del self.headers['Set-Cookie']
                else:
                    raise ValueError('You can\'t remove a cookie that doesn\'t exist!')
        else:
            raise ValueError('You can\'t remove a cookie that doesn\'t exist!')

    def serializeHeaders(self):
        '''This gets just the headers in a binary string.'''
        
        headers = []
        
        #gets the headers
        for key in self.headers.keys():
            if type(self.headers[key]) == list:
                for item in self.headers[key]:
                    headers.append(key.encode(self.charset) + b': ' + str(item).encode(self.charset))
            else:
                headers.append(key.encode(self.charset) + b': ' + str(self.headers[key]).encode(self.charset))
                
        #joins the headers
        headers = b'\r\n'.join(headers)

        return headers

    __bytes__ = serializeHeaders    

    def serialize(self, content):
        '''This gets the fully binary string including headers and the content.'''
        return b'HTTP/1.1 ' + self.convertBytes(self.statusCode) + b' ' + self.convertBytes(self.reasonPhrase) + b'\r\n' + self.serializeHeaders() + b'\r\n\r\n' + content

    def convertBytes(self, value):
        '''Encodes value and converts it to bytes.'''
        if isinstance(value, str):
            return bytes(value, encoding=self.charset)
        elif isinstance(value, bytes):
            return value

        return bytes(str(value), encoding=self.charset)

class HTTPResponse(HTTPResponseBase):
    '''Handles the HTTP responses and content.'''

    def __init__(self, request=None, content=b'', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

        self.content = content 

    def __bytes__(self):
        content = (self.content if self.content != b'None' else b'')
        return self.serialize(content)

    @property
    def content(self):
        return b"".join(self._content)

    @content.setter
    def content(self, value):
        self._content = [self.convertBytes(value)]
        self.headers['Content-Length', None] = str(len(self.content))

class JSONResponse(HTTPResponse):
    '''Handles the HTTP responses and json.'''

    def __init__(self, request=None, data={}, **kwargs):
        super().__init__(**kwargs)
        data = json.dumps(data)
        self.content = data

        self.request = request
        self.headers['Content-Type', None] = f'application/json; charset={self.charset}'

    @property
    def data(self):
        return self.content

class FileResponse(HTTPResponse):
    '''Handles the HTTP responses and file.'''

    def __init__(self, request=None, fileObj=None, mimeType=None, **kwargs):
        super().__init__(**kwargs)
        self.content = fileObj.read()
        self.mimeType = mimeType

        self.request = request

        #add mimetype to content-type
        if self.mimeType is not None:
            self.headers['Content-Type', None] = f'{self.mimeType}; charset={self.charset}'
        else:
            mt = mimetypes.guess_type(fileObj.name)
            if mt[0] is not None:
                self.headers['Content-Type', None] = f'{mt[0]}; charset={self.charset}'
            else:
                self.headers['Content-Type', None] = f'application/octet-stream; charset={self.charset}'

        self.headers['Content-Length', None] = str(len(self.fileObj))

    @property
    def fileObj(self):
        return self.content

class HTTPResponseRedirectBase(HTTPResponse):
    '''The base redirect class'''
    def __init__(self, redirectTo, **kwargs):
        super().__init__(**kwargs)
        self.headers['Location'] = redirectTo

class HTTPResponseRedirect(HTTPResponseRedirectBase):
    '''A Http response redirect, takes one argument: redirectTo'''
    statusCode = 302

class HTTPResponsePermenentRedirect(HTTPResponseRedirectBase):
    '''A Http response permanent redirect, takes one argument: redirectTo'''
    statusCode = 301

def render(request=None, filePath: str=None, context: dict={}, charset=None, status=None, reason=None):
    '''
    Returns a HTTPResponse with the rendered template, this uses jinja2 as it's defualt.
    it takes 7 arguments:
     - request - A Request object. 
     - filePath - The file path to the template. 
     - context - A dict with all the varibles for the template. 
     - charset - The charset for the response. 
     - status - The status code for the response. 
     - reason - The status reason for the response. 
    '''
    templateRender = renderTemplate(filePath=filePath, context=context)
    return HTTPResponse(request, templateRender, charset=charset, status=status, reason=reason)

def redirect(redirectTo: str, permanent: bool=False):
    """
    A Http redirect, takes 2 arguments:
     - redirectTo - the place that you want to redirect to. 
     - permentent - if the redirect is permanent. 
    """
    return (HTTPResponseRedirect(redirectTo) if permanent == False else HTTPResponsePermenentRedirect(redirectTo))
    