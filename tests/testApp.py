from waffleweb import WaffleApp
from waffleweb.response import HTTPResponse

app = WaffleApp('test')

@app.route('/test/')
def test(request):
    return HTTPResponse('Test')

@app.route('/test2/')
def test2(request):
    return HTTPResponse('Test2')

