from waffleweb import WaffleApp
from waffleweb.response import HTTPResponse, JSONResponse

MathAPI = WaffleApp('MathAPI')

@MathAPI.route('math/<operator:str>/<num1:int>/<num2:int>', 'math')
def math(request, operator, num1, num2):
    if operator == 'add':
        result = {'answer': int(num1) + int(num1)}
    elif operator == 'subtract':
        result = {'answer': int(num1) - int(num1)}
    elif operator == 'multiply':
        result = {'answer': int(num1) * int(num1)}
    elif operator == 'divide':
        result = {'answer': int(num1) / int(num1)}
    else:
        result = {'error': 'Unknown operator'}

    return JSONResponse(result)