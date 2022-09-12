import mimetypes
import waffleweb

from pathlib import Path
from waffleweb.response import HTTP404, FileResponse
from waffleweb.defaults import DEFUALT_STATIC_DIR

def findStatic(path: str):
    '''Finds a static file\'s path. '''

    staticDir = waffleweb.currentRunningApp.settings.get('STATIC_DIR', DEFUALT_STATIC_DIR)
    staticDir = staticDir.strip('/')

    file = path.strip('/')
    
    if file == '':
        staticPath = Path(f'./{file}').resolve()
    else:
        staticPath = Path(f'./{staticDir}/{file}').resolve()

    return staticPath

def openStatic(file, mode='rb', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    '''Returns a file, takes the same arguments as open()'''

    staticFinder = waffleweb.currentRunningApp.settings.get('DEFUALT_STATIC_FINDER', findStatic)
   
    return open(staticFinder(file), mode, buffering, encoding, errors, newline, closefd, opener)

def getStaticFileResponse(request, root, ext): 
    '''Finds a static file, returns a FileResponse'''
    
    path = root + ext
    
    try:
        with openStatic(path, 'rb') as f:
            mt = mimetypes.guess_type(path)
            if mt[0] is not None:
                return FileResponse(request, f, mimeType=mt[0])
            else:
                return FileResponse(request, f, mimeType='application/octet-stream')
    except FileNotFoundError:
        raise HTTP404
