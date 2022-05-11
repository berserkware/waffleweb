import waffleweb

from jinja2 import Environment, FileSystemLoader, ModuleLoader, select_autoescape

def _getEnviromentModule(module: str):
    '''Gets a jinja Enviroment with the loader being PackageLoader.'''
    env = Environment(
        loader=ModuleLoader(module),
        autoescape=select_autoescape,
    )
    return env

def _getEnviromentFile():
    '''Gets a jinja Enviroment with the loader being FileSystemLoader.'''
    env = Environment(
        loader=FileSystemLoader(searchpath=f"./{waffleweb.defaults.DEFUALT_TEMPLATE_DIR}"),
        autoescape=select_autoescape,
    )
    return env

def renderTemplate(filePath: str, context: dict, moduleName: str=None, loaderTypeFile: bool=True):
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
    
def renderErrorPage(mainMessage: str, subMessage: str, traceback: str):
    '''
    Renders and error page for debug, it takes 3 arguments:
        mainMessage
        subMessage
        traceback
    '''

    return f'''
        <h1>{mainMessage}</h1>
        <h2>{subMessage}</h2>
        <h3>{traceback}</h3>
    '''