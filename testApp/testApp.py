from waffleweb import WaffleApp
from waffleweb.response import HTTPResponse, JSONResponse

testApp = WaffleApp('testApp')

@testApp.route('/', 'index')
def index(request):
    return HTTPResponse(f"<title>Waffleweb</title><h1>This webiste is made with waffleweb!</h1><p>{request.userAgent}</p>")

@testApp.route('jsontest/jsontestagain', 'jsonTest')
def jsonTest(request):
    return JSONResponse({
    "number": 1240,
})

@testApp.route('argtest/<testArg:str>', 'argTest')
def argTest(request, testArg):
    response = {'testArg': testArg}

    return JSONResponse(response)