import waffleweb
import importlib
import os

try:
    settings = importlib.import_module('settings')
except ModuleNotFoundError:
    settings = None

from waffleweb.exceptions import ViewNotFoundError
from jinja2 import Environment, FileSystemLoader, select_autoescape

def getRelativeUrl(viewName: str, **kwargs):
    app = waffleweb.currentRunningApp
    
    for view in app.views:
        if view.name == viewName:
            if view.hasPathHasArgs() == False:
                return f'{view.unstripedPath}'
            else:
                finalPath = []
                
                for part in view.splitPath:
                    if type(part) == list:
                        argName = part[0]
                        try:
                            finalPath.append(kwargs[argName])
                        except KeyError:
                            raise KeyError(f'Value for arg \"{argName}\" not found in kwargs.')
                    else:
                        finalPath.append(part)
                    
                if view.unstripedPath.endswith('/'):
                    return f'/{"/".join(finalPath)}/'
                else:
                    return f'/{"/".join(finalPath)}'
                        
    #if cant find view, raise error
    raise ViewNotFoundError(f'View {viewName} could not be found.')

def getEnvironmentFile() -> Environment:
    '''Gets a jinja Enviroment with the loader being FileSystemLoader.'''

    #Gets the template directory from the users settings files.
    templateDir = waffleweb.currentRunningApp.settings.get('TEMPLATE_DIR', waffleweb.defaults.DEFUALT_TEMPLATE_DIR)

    env = Environment(
        loader=FileSystemLoader(searchpath=templateDir),
        autoescape=select_autoescape,
    )

    #Gets user supplied template functions
    templateFunctions = waffleweb.currentRunningApp.settings.get('TEMPLATE_FUNCTIONS', {})

    #Adds user supplied template functions
    for key, value in templateFunctions:
        env.globals[key] = value

    env.globals['getRelativeUrl'] = getRelativeUrl
    return env

def renderTemplate(filePath: str, context: dict={}) -> str:
    '''
    renders a template using jinja2, takes three arguments:
     - filepath - required - the file path to the template
     - context - the variables for the template
    '''

    templateRenderer = waffleweb.currentRunningApp.settings.get('TEMPLATE_RENDERER')

    if templateRenderer is not None:
        return templateRenderer(filePath, context)
    else:
        env = waffleweb.currentRunningApp.settings.get('JINJA_ENVIROMENT', getEnvironmentFile())

        #gets the template render
        template = env.get_template(filePath)
        templateRender = template.render(**context)

        return templateRender
    
def renderErrorPage(mainMessage: str, subMessage: str='', traceback: str='') -> str:
    '''
    Renders an error page for debug, it takes 3 arguments:
     - mainMessage
     - subMessage - optional
     - tracebackList - optional
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
        subMessage=(f'<h2 style="color: #7a7a7a; display: block; margin:15px; padding:0px;">{subMessage}</h2>' if subMessage != '' else ''),
        traceback=(f'''
                <fieldset style="display: block; margin:15px; padding:0px;">
                    <legend style="margin-left:15px; margin-top:0px margin-bottom:0px padding:0px;"><h2 style="margin:0; padding:0px;">Traceback</h2></legend>
                    <h3 style="margin-left:15px; margin-top:5px; margin-bottom:10px; padding:0px;">{traceback}</h3>
                </fieldset>
                ''' if traceback != '' else ''),
        )
