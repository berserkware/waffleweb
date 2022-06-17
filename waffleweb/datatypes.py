class MultiValueOneKeyDict(dict):
    def __init__(self, data={}, *args, **kwargs):
        super(MultiValueOneKeyDict, self).__init__(*args, **kwargs)
        
        self._data = {}
        
        #Turns all the values to lists
        for key in data.keys():
            if type(data[key]) == list:
                self._data[key] = data[key]
            else:
                self._data[key] = [data[key]]
                
    def __dict__(self):
        return self._data
        
    def __len__(self):
        return len(self._data)
                
    def __repr__(self):
        return repr(self._data)
                
    def __getitem__(self, values):
        if type(values) == tuple:
            if len(values) != 2:
                raise IndexError('You have to have a key and an index or a just a key')
            return self._data[str(values[0])][int(values[1])]
        else:
            if len(self._data[str(values)]) == 1:
                return self._data[str(values)][0]
            else:
                return self._data[str(values)]
                
    def get(self, keyname, index=None, default=None):
        try:
            if index:
                return self[keyname, index]
            else:
                return self[keyname]
        except KeyError:
            return default

    def __setitem__(self, values, value):
        if type(values) == tuple:
            if len(values) != 2:
                raise IndexError('You have to have a key and an index or a just a key')
            
            if str(values[0]) in self._data or values[1] is None:
                if values[1] is not None:
                    self._data[str(values[0])][int(values[1])] = value
                else:
                    if type(value) == list:
                        self._data[str(values[0])] = value
                    else:
                        self._data[str(values[0])] = [value]
            else:
                raise IndexError('You can\'t have a index if your key doesn\'t exists in the dictionary.')
        else:
            if type(value) == list:
                if str(values) in self._data.keys():
                    self._data[str(values)] = self._data[str(values)] + value
                else:
                    self._data[str(values)] = value 
            else:
                if str(values) in self._data.keys():
                    self._data[str(values)].append(value)
                else:
                    self._data[str(values)] = [value]
                
    def setdefault(self, keyname, index=None, value=None):
        if keyname in self.keys():
            if index is not None:
                return self[keyname, index]
            else:
                return self[keyname]
        else:
            if index is not None:
                self[keyname, index] = value
            else:
                self[keyname] = value
                
    def __delitem__(self, values):
        if type(values) == tuple:
            if len(values) != 2:
                raise IndexError('You have to have a key and an index or a just a key')
            del self._data[values[0]][int(values[1])]
        else:
            del self._data[str(values)]
            
    def pop(self, keyname, index=None, default=None):
        try:
            if index is not None:
                value = str(self[keyname, index])
                del self[keyname, index]
                return value
            else:
                value = repr(self[keyname, index])
                del self[keyname]
                return value
        except KeyError:
            return default
            
    def keys(self):
        return self._data.keys()
        
    def items(self):
        return self._data.items()
        
    def copy(self):
        return self._data.copy()