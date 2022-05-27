class File:
    """
    A file, takes 4 arguments:
     - name - Name of file
     - data - the file data
     - contentType - the content type of the file
     - size - the size of the file
    """

    def __init__(self, name, data, contentType, size=None):
        self.name = name
        self.data = data
        self.contentType = contentType
        self.size = size