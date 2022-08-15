import importlib
try:
    settings = importlib.import_module('settings')
except ModuleNotFoundError:
    settings = None

def getFromSettings(var:str, default=None):
    obj = default
    if hasattr(settings, var):
        obj = getattr(settings, var)
    return obj
