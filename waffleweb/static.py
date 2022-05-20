import os
import mimetypes
import importlib
try:
    settings = importlib.import_module('settings')
except ModuleNotFoundError:
    settings = None

from pathlib import Path
from waffleweb.response import HTTP404, FileResponse, HTTPResponse
from waffleweb.defaults import DEFUALT_STATIC_DIR

def findStatic(path, mode='rb', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    staticDir = DEFUALT_STATIC_DIR.strip('/')
    if hasattr(settings, 'STATIC_DIR'):
        staticDir = getattr(settings, 'STATIC_DIR').strip('/')

    file = path.strip('/')

    path = Path(f'./{staticDir}/{file}').resolve()

    return open(path, mode, buffering, encoding, errors, newline, closefd, opener)

def openStatic(file, mode='rb', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    '''Returns a file, takes the same arguments as open()'''
    staticFinder = findStatic
    if hasattr(settings, 'DEFUALT_STATIC_FINDER'):
        staticFinder = getattr(settings, 'DEFUALT_STATIC_FINDER')
    
    return staticFinder(file, mode, buffering, encoding, errors, newline, closefd, opener)

class StaticHandler:
    def __init__(self, request, root, splitRoot, ext):
        self.request = request
        self.path = root + ext
        self.root, self.splitRoot, self.ext = root, splitRoot, ext

    def findFile(self): 
        try:
            with openStatic(self.path, 'rb') as f:
                mt = mimetypes.guess_type(self.root + self.ext)
                if mt[0] is not None:
                    return FileResponse(self.request, f, mimeType=mt[0])
                else:
                    return FileResponse(self.request, f, mimeType='application/octet-stream')
        except FileNotFoundError:
            raise HTTP404