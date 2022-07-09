class AppMiddletest():
    def after(response):
        if response.request.path == '/':
            response.content = 'middlewareified'
        return response

    def before(request):
        request.POST = {}
        return request