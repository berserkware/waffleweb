from waffleweb import WaffleApp
from waffleweb.response import HttpResponse

testApp = WaffleApp('testApp')

@testApp.route('/', 'index')
def index(request):
    return HttpResponse(f"<title>Waffleweb</title><h1>This webiste is made with waffleweb!</h1><p>{request.userAgent}</p>")

@testApp.route('page1/', 'page1')
def page1(request):
    return HttpResponse("Welcome to the page one")