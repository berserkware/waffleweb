from waffleweb import app
from waffleweb.response import HTTPResponse

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
    
@app.route('/randomStatus')
def st(request):
    return HTTPResponse(request, 'Random status', status=220)
    
@app.route('/statusNoHandler')
def snh(request):
    return HTTPResponse(request, 'status but no handler.', status=123)
    
@app.errorHandler(404)
def view404(request):
    return HTTPResponse(request, '404 Page Handler', status=404)
    
@app.errorHandler(220)
def view220(request):
    return HTTPResponse(request, '220 Page', status=220)