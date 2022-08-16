class AppMiddletest():
    def after(response):
        response.content = 'middlewareified'
        return response

    def before(request):
        request.META['TEST_HEADER', 0] = 'value2'
        return request
