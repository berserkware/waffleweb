import waffleweb.defaults
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

def getEnviroment():
    env = Environment(
        loader=FileSystemLoader(searchpath=f"./{waffleweb.defaults.DEFUALT_TEMPLATE_DIR}"),
        autoescape=select_autoescape,
    )
    return env