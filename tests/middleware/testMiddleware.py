class TestMiddleware:
    def after(response):
        response.headers['middlewareHeader', None] = 'value'
        return response
        
    def before(request):
        request.META['middlewareHeader2'] = 'value'
        return request