import waffleweb
import importlib
try:
    settings = importlib.import_module('settings')
except ModuleNotFoundError:
    settings = None

from jinja2 import Environment, FileSystemLoader, ModuleLoader, select_autoescape

def _getEnviromentModule(module: str) -> Environment:
    '''Gets a jinja Enviroment with the loader being PackageLoader.'''
    env = Environment(
        loader=ModuleLoader(module),
        autoescape=select_autoescape,
    )
    return env

def _getEnviromentFile() -> Environment:
    '''Gets a jinja Enviroment with the loader being FileSystemLoader.'''

    #Gets the template directory
    templateDir = waffleweb.defaults.DEFUALT_TEMPLATE_DIR
    if hasattr(settings, 'TEMPLATE_DIR'):
        templateDir = getattr(settings, 'TEMPLATE_DIR')

    env = Environment(
        loader=FileSystemLoader(searchpath=templateDir),
        autoescape=select_autoescape,
    )
    return env

def renderTemplate(filePath: str, context: dict={}, moduleName: str=None, loaderTypeFile: bool=True) -> str:
    '''
    renders a template using jinja2, takes four arguments:
        filepath - required - the file path to the template
        context - the variables for the template
        loaderTypeFile - default:True - if True uses loader FileSystemLoader if False use loader ModuleLoader.
        moduleName - Needed if your loaderTypeFile == False
    '''

    #gets the enviroment
    if loaderTypeFile == True:
        env = _getEnviromentFile()
    else:
        env = _getEnviromentModule(moduleName)

    #gets the template render
    template = env.get_template(filePath)
    templateRender = template.render(**context)

    return templateRender
    
def renderErrorPage(mainMessage: str, subMessage: str=None, traceback: str=None) -> str:
    '''
    Renders and error page for debug, it takes 3 arguments:
        mainMessage
        subMessage - optional
        traceback - optional
    '''

    return f'''
        <title>{mainMessage}</title>
        <h1>{mainMessage}</h1>
        {(f'<h2>{subMessage}</h2>' if subMessage is not None else '')}
        {(f'<h3>{traceback}</h3>' if traceback is not None else '')}
    '''