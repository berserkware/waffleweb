from waffleweb import WaffleApp
from waffleweb.response import JSONResponse

app = WaffleApp('test')

@app.route('/argTestConvertion/<stringArg:str>/<intArg:int>/<floatArg:float>/', 'argConvertionTest')
def argConvertionTest(request, stringArg, intArg, floatArg):
    return JSONResponse({
        'stringArg': stringArg,
        'intArg': intArg,
        'floatArg': floatArg,
        }, request=request)

@app.route('/URLFindTest/pathThingOne/pathThingTwo/', 'URLFindTest')
def argConvertionTest(request, stringArg, intArg, floatArg):
    return JSONResponse({
        'stringArg': stringArg,
        'intArg': intArg,
        'floatArg': floatArg,
        }, request=request)