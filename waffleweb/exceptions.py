class AppNotFoundError(Exception):
    pass

class AppImportError(Exception):
    pass

class ViewNotFoundError(Exception):
    pass

class MiddlewareNotFoundError(Exception):
    pass

class MiddlewareImportError(Exception):
    pass

class ParsingError(Exception):
    pass