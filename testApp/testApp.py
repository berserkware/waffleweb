from waffleweb import WaffleApp
from waffleweb.response import HttpResponse

testApp = WaffleApp('testApp')

@testApp.route('/', 'index')
def index(request):
    return HttpResponse("Welcome to the index page")

@testApp.route('page1/bollocks', 'page1')
def page1(request):
    return HttpResponse("Welcome to the page one")