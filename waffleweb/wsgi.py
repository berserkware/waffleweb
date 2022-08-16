def getResponseHeaders(response):
    responseHeaders = []

    headers = response.headers

    #gets the headers
    for key in headers.keys():
        if type(headers[key]) == list:
            for item in headers[key]:
                responseHeaders.append((key, str(item)))
        else:
            responseHeaders.append((key, str(headers[key])))

    return responseHeaders

def getResponseStatus(response):
    return f'{response.statusCode} {response.reasonPhrase}'
