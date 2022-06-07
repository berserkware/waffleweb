from waffleweb import WaffleApp
from waffleweb.response import HTTPResponse

app = WaffleApp('test')

@app.route('/test/')
def test(request):
    return HTTPResponse(request, 'Test')

@app.route('/test2/')
def test2(request):
    return HTTPResponse(request, 'Test2')

@app.route('BasicTest/')
def BasicTest(request):
    return HTTPResponse(request)
    
@app.route('/WithArgsTest/<testArg1:str>/test/<testArg2:str>/')
def WithArgsTest(request, testArg1, testArg2):
    return HTTPResponse(request)