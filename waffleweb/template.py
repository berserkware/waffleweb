import waffleweb
import importlib
try:
    settings = importlib.import_module('settings')
except ModuleNotFoundError:
    settings = None

from jinja2 import Environment, FileSystemLoader, ModuleLoader, select_autoescape

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

def renderTemplate(filePath: str, context: dict={}) -> str:
    '''
    renders a template using jinja2, takes three arguments::
        filepath - required - the file path to the template

        context - the variables for the template
    '''

    if hasattr(settings, 'TEMPLATE_RENDERER'):
        renderer = getattr(settings, 'TEMPLATE_RENDERER')

        return renderer(filePath, context)
    else:
        #gets the enviroment
        env = _getEnviromentFile()

        #gets the template render
        template = env.get_template(filePath)
        templateRender = template.render(**context)

        return templateRender
    
def renderErrorPage(mainMessage: str, subMessage: str=None, traceback: str=None) -> str:
    '''
    Renders and error page for debug, it takes 3 arguments::
        mainMessage

        subMessage - optional

        traceback - optional
    '''

    return '''
        <!DOCTYPE html>
        <html>
            <head>
                <title>{mainMessage}</title>
            </head>
            
            <body style="font-family: Arial, Helvetica, sans-serif; margin:0px; padding:0;">
                <h1 style="background-color: #f6c486; display: block; margin:0px; padding:15px;">{mainMessage}</h1>
                {subMessage}
                {traceback}
            </body>
        </html>
    '''.format(
        mainMessage=mainMessage,
        subMessage=(f'<h2 style="color: #7a7a7a; display: block; margin:15px; padding:0px;">{subMessage}</h2>' if subMessage is not None else ''),
        traceback=(f'''
        <fieldset style="display: block; margin:15px; padding:0px;">
            <legend style="margin-left:15px; margin-top:0px margin-bottom:0px padding:0px;"><h2 style="margin:0; padding:0px;">Traceback</h2></legend>
            <h3 style="margin-left:15px; margin-top:5px; margin-bottom:10px; padding:0px;">{traceback}</h3>
        </fieldset>
        ''' if traceback is not None else ''),
        )