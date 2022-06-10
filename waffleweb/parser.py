from waffleweb.files import File

def parsePost(body, contentType) -> dict:
    postData = {}
    files = {}
    
    contentTypeMime = contentType.split(';')[0]

    #Spits the form values and adds them to a dictionary if Content-Type is 'application/x-www-form-urlencoded'
    if contentTypeMime == 'application/x-www-form-urlencoded':
        formValues = body.split('&')

        #For every form value add it to a dictionary called postData
        for value in formValues:
            try:
                key, value = value.split('=')
                postData[str(key.strip('\n'))] = str(value.strip('\n'))
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
        splitFormValues = body.split('--' + boundary)

        #goes through all the split values
        for formValue in splitFormValues:
            if formValue != '\n' and formValue != '--\n' and formValue != '' and formValue != '--\r\n':
                #splits the data into its seporate headers and removes empty items
                dataWithSpaces = formValue.split('\n')
                data = []
                for i in dataWithSpaces:
                    if i != '' and i != '\r':
                        data.append(i)

                headers = {}
                for field in data[0].split('\n'):
                    headers[field.split(': ')[0].upper().replace('-', '_')] = field.split(': ')[1]
                
                isFile = False
                name = ''
                #gets stuff from the content disposation
                cd = headers['CONTENT_DISPOSITION'].split('; ')
                for i in cd:
                    if i.split('=')[0] == 'name':
                        name = i.split('=')[1].strip('\r').strip('"')
                    elif i.split('=')[0] == 'filename':
                        size = len(str(data[-1]))

                        contentType = headers.get('CONTENT_TYPE')
                        files[str(name)] = File(i.split('=')[1].strip('\r').strip('"'), data[-1].strip('\r'), (contentType if contentType != -1 else 'text/plain'), size)
                        isFile = True

                if isFile == False:
                    #adds to postData
                    postData[str(name)] = data[-1].strip('\r')

    return (postData, files)

def parseBody(request: str) -> str:
    splitContent = []
    isContent = False

    #this splits the request by the \r
    for line in request.split('\r'):
        #check if isContent is True to start adding to the content
        if isContent == True:
            splitContent.append(line)

        #checks if the line is = '\n'. this splits the request into content and header
        if line == '\n':
            isContent = True

    #returns the joins content
    return ''.join(splitContent)

def parseHeaders(request: str) -> dict:
    headerDict = {}
    #Gets all the headers
    for line in request.split('\r'):
        if len(line.split(': ')) == 2:    
            splitLine = line.strip().split(' ')
            headerDict[str(splitLine[0][:(len(splitLine[0]) - 1)]).upper().replace('-', '_')] = ' '.join(splitLine[1:])
    
        if line == '\n':
            break

    return headerDict