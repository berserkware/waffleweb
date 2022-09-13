from waffleweb.exceptions import ParsingError
from waffleweb.files import File
from waffleweb.datatypes import MultiValueOneKeyDict
from urllib.parse import unquote, urlparse
import os

def parsePost(body: bytes, contentType: str) -> dict:
    postData = {}
    files = {}
    
    try:
        contentTypeMime = contentType.split(';')[0]

        #Spits the form values and adds them to a dictionary if Content-Type is 'application/x-www-form-urlencoded'
        if contentTypeMime == 'application/x-www-form-urlencoded':
            formValues = body.split(b'&')

            #For every form value add it to a dictionary called postData
            for value in formValues:
                try:
                    key, value = value.split(b'=')
                    value = value.strip(b'\n').decode().replace('+', ' ')
                    key = key.strip(b'\n').decode().replace('+', ' ')
                    postData[unquote(key)] = unquote(value)
                except ValueError:
                    pass

        #If the contentType is equal to 'multipart/form-data' split it and add it to a dictionary
        elif contentTypeMime == 'multipart/form-data':
            #gets the boundry
            contentTypeHeader = contentType.split(';')
            boundary = 'boundary'

            for index, keyvalue in enumerate(contentTypeHeader):
                if index != 0:
                    key, value = keyvalue.split('=')
                    if key.strip() == 'boundary':
                        boundary = value

            #splits the form values by the boundry
            splitFormValues = body.split(b'--' + boundary.encode())

            #goes through all the split values
            for formValue in splitFormValues:
                if formValue != b'\n' and formValue != b'--\n' and formValue != b'' and formValue != b'--\r\n':
                    #Gets the headers and data

                    headersAndData = formValue.split(b'\r\n\r\n')
                        
                    if len(headersAndData) == 1:
                        headersAndData = formValue.split(b'\n\n')
                        headersStr = headersAndData[0].strip(b'\r\n').strip(b'\n')
                        data = b'\n\n'.join(headersAndData[1:]).strip(b'\r\n').strip(b'\n')
                    else:
                        headersStr = headersAndData[0].strip(b'\r\n').strip(b'\n')
                        data = b'\r\n\r\n'.join(headersAndData[1:]).strip(b'\r\n').strip(b'\n')

                    headers = {}
                    for field in headersStr.split(b'\n'):
                        if field != b'\r':
                            headers[field.split(b': ')[0].upper().replace(b'-', b'_').decode()] = field.split(b': ')[1].decode()
                    
                    isFile = False
                    name = ''
                    #gets stuff from the content disposation
                    contentDisposition = headers['CONTENT_DISPOSITION'].split('; ')
                    for part in contentDisposition:
                        if part.split('=')[0] == 'name':
                            name = part.split('=')[1].strip('\r').strip('"')
                        elif part.split('=')[0] == 'filename':
                            size = len(data)

                            #Gets the data of the file
                            contentType = headers.get('CONTENT_TYPE', 'text/plain')
                            #Gets the name of the file, and converts it into proper charecters
                            fileName = unquote(part.split('=')[1].strip('\r').strip('"'))
                            data = data.strip(b'\r')
                            
                            files[str(name)] = File(fileName, data, contentType, size)
                            isFile = True

                    if isFile == False:
                        #adds to postData
                        postData[unquote(str(name))] = unquote(data.strip(b'\r').decode())
    except (IndexError, ValueError, KeyError):
        raise ParsingError('A problem occured while parsing the POST data.')

    return (postData, files)

def parseBody(request: bytes) -> bytes:
    try:
        splitContent = []
        isContent = False

        #this splits the request by the \r
        for line in request.split(b'\r'):
            #check if isContent is True to start adding to the content
            if isContent == True:
                splitContent.append(line)

            #checks if the line is = '\n'. this splits the request into content and header
            if line == b'\n':
                isContent = True

        #returns the joins content
        content = b''.join(splitContent)
        if content == b'\n':
            return b''
        else:
            return content
    except (IndexError, ValueError):
        raise ParsingError('A problem occured while parsing the body.')

def parseHeaders(request: bytes) -> MultiValueOneKeyDict:
    try:
        headerDict = MultiValueOneKeyDict()
        
        #Gets all the headers
        for line in request.split(b'\r'):
            line = line.decode()
            
            if len(line.split(': ')) == 2:    
                splitLine = line.strip().split(' ')
                #This gets the name of the header without changing it
                rawHeaderName = str(splitLine[0].strip(':'))
                
                #This makes all letters upper case, and replaces the hypens with a low line. Header-Name gets turned into HEADER_NAME.
                #This is to make it the same as the wsgi headers
                headerName = rawHeaderName.upper().replace('-', '_')
                
                #Joins the header line, except for the header name.
                headerValue = ' '.join(splitLine[1:])
                
                headerDict[headerName] = headerValue
        
            if line == '\n':
                break

        return headerDict
    except (IndexError, ValueError):
        raise ParsingError('A problem occured while parsing the headers.')

def splitURL(path: str):
    """Splits a URL into three parts: root, split root and extension."""

    reqPath = urlparse(path).path

    #gets the root and file extenstion
    root, ext = os.path.splitext(reqPath)
    splitRoot = root.strip('/').split('/')

    return (root, splitRoot, ext)


def parseURLParameters(path: str):
    urlParams = {}

    splitPath = path.split('?')

    argString = '?'.join(splitPath[1:])

    splitArgs = argString.split('&')

    for arg in splitArgs:
        try:
            name, value = arg.split('=')
            urlParams[str(name)] = str(value)
        except ValueError:
            pass

    return urlParams

