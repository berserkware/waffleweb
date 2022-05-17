import os
import mimetypes

from pathlib import Path
from waffleweb.response import HTTP404, FileResponse, HTTPResponse

class StaticHandler:
    def __init__(self, request, root, splitRoot, ext):
        self.request = request
        self.root, self.splitRoot, self.ext = root, splitRoot, ext

    def findFile(self):
        
        path = Path(f'./static/{self.root}{self.ext}').resolve()
        try:
            with open(path, 'rb') as f:
                mt = mimetypes.guess_type(self.root + self.ext)
                if mt[0] is not None:
                    return FileResponse(self.request, f, mimeType=mt[0])
                else:
                    return FileResponse(self.request, f, mimeType='application/octet-stream')
        except FileNotFoundError:
            raise HTTP404