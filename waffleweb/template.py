import waffleweb

from waffleweb.exceptions import ViewNotFoundError
from jinja2 import Environment, FileSystemLoader, select_autoescape

def getRelativeUrl(viewName: str, **kwargs):
    app = waffleweb.currentWorkingApp
    
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
    templateDir = waffleweb.currentWorkingApp.settings.get('TEMPLATE_DIR', waffleweb.defaults.DEFUALT_TEMPLATE_DIR)

    env = Environment(
        loader=FileSystemLoader(searchpath=templateDir),
        autoescape=select_autoescape,
    )

    #Gets user supplied template functions
    templateFunctions = waffleweb.currentWorkingApp.settings.get('TEMPLATE_FUNCTIONS', {})

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

    templateRenderer = waffleweb.currentWorkingApp.settings.get('TEMPLATE_RENDERER')

    if templateRenderer is not None:
        return templateRenderer(filePath, context)
    else:
        env = waffleweb.currentWorkingApp.settings.get('JINJA_ENVIROMENT', getEnvironmentFile())

        #gets the template render
        template = env.get_template(filePath)
        templateRender = template.render(**context)

        return templateRender
