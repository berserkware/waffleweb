def getResponseHeaders(response) -> list[tuple]:
    """This gets the headers of a response. It puts headers into tuples, and then into a list."""

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

def getResponseStatus(response) -> str:
    """This gets the code and status of a response, and puts it into a string"""
    return f'{response.statusCode} {response.reasonPhrase}'
