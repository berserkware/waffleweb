from waffleweb import WaffleApp
from waffleweb.response import HTTPResponse, JSONResponse

MathAPI = WaffleApp('MathAPI')

@MathAPI.route('/math/', 'math')
def math(request):
    return HTTPResponse("""
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
    """)

@MathAPI.route('math/<operator:str>/<num1:int>/<num2:int>', 'basicMath')
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

    return JSONResponse(result)