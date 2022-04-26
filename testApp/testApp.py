from waffleweb import WaffleApp
from waffleweb.response import FileResponse, HTTPResponse, JSONResponse

testApp = WaffleApp('testApp')

@testApp.route('/', 'index')
def index(request):
    return HTTPResponse(f"<link rel=\"stylesheet\" href=\"\\filetest\"><title>Waffleweb</title><h1>This webiste is made with waffleweb!</h1><p>{request.userAgent}</p>")

@testApp.route('jsontest/jsontestagain', 'jsonTest')
def jsonTest(request):
    return JSONResponse({
    "number": 1240,
})

@testApp.route('argtest/<testArg:str>', 'argTest')
def argTest(request, testArg):
    response = {'testArg': testArg}
    return JSONResponse(response)

@testApp.route('filetest', 'fileTest')
def argTest(request):
    with open('static/testCSS.css', 'rb') as f:
        return FileResponse(f, 'text/css')

@testApp.route('testimg', 'testImg')
def argTest(request):
    with open('static/testImg.jpg', 'rb') as f:
        return FileResponse(f, 'image/jpeg')