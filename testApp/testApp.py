from waffleweb import WaffleApp
from waffleweb.response import HTTPResponse, JSONResponse

testApp = WaffleApp('testApp')

@testApp.route('/', 'index')
def index(request):
    return HTTPResponse(f"<title>Waffleweb</title><h1>This webiste is made with waffleweb!</h1><p>{request.userAgent}</p>")

@testApp.route('testpage/', 'testpage')
def page1(request):
    return HTTPResponse('''<html>
                                <head>
                                    <title>Div Align Attribbute</title>
                                </head>
                                <body>
                                    <div align="left">
                                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
                                    labore et dolore magna aliqua.
                                    </div>
                                    <div align="right">
                                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
                                    labore et dolore magna aliqua.
                                    </div>
                                    <div align="center">
                                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
                                    labore et dolore magna aliqua.
                                    </div>
                                    <div align="justify">
                                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
                                    labore et dolore magna aliqua.
                                    </div>
                                </body>
                            </html>
''')

@testApp.route('jsontest/', 'jsonTest')
def jsonTest(request):
    return JSONResponse({
    "number": 1240,
})