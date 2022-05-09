from waffleweb import WaffleApp
from waffleweb.response import HTTPResponse, JSONResponse, render

MathAPI = WaffleApp('MathAPI')

@MathAPI.route('/math/', 'math')
def math(request):
    return HTTPResponse(request, """
        <!DOCTYPE html>
        <html>
            <head>
                <title>Math API</title>
            </head>
            <body>
                <h1>Welcome to the Math API</h1>
                <h3>Usage:</h3>
                <code>localhost:8080/math/[operator]/[num1]/[num2]/</code>
                <p>Availiable Operators: add, subtract, multiply, divide</p>
            </body>
        </html>
    """,)

@MathAPI.route('math/<operator:str>/<num1:int>/<num2:int>', 'basicMath', ['GET', 'POST'])
def basicMath(request, operator, num1, num2):
    if operator == 'add':
        result = {'answer': num1 + num2}
    elif operator == 'subtract':
        result = {'answer': num1 - num2}
    elif operator == 'multiply':
        result = {'answer': num1 * num2}
    elif operator == 'divide':
        result = {'answer': num1 / num2}
    else:
        result = {'error': 'Unknown operator'}

    return JSONResponse(request, result)

@MathAPI.route('math/postTest', 'postTest', ['POST'])
def postTest(request):
    return HTTPResponse(request, request.postData)

@MathAPI.route('cookieTest')
def cookieTest(request):
    res = HTTPResponse(request, content='testing 123')
    res.setCookie('testCookie', 'testVal')
    return res

@MathAPI.route('templateTest')
def testPlate(request):
    return render(request, 'testPlate.html')