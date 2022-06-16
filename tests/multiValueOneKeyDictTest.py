import unittest
from waffleweb.datatypes import MultiValueOneKeyDict

class CreateTest(unittest.TestCase):
    def test_dictIncorrect(self):
        self.assertEqual(MultiValueOneKeyDict({'data': 'value'})._data, {'data': ['value']})
        
    def test_dictCorrect(self):
        self.assertEqual(MultiValueOneKeyDict({'data': ['value']})._data, {'data': ['value']})
        
    def test_empty(self):
        self.assertEqual(MultiValueOneKeyDict(), {})
        
class GetTest(unittest.TestCase):
    
    def test_findWithOneValueNoIndex(self):
        dic = MultiValueOneKeyDict({'data': ['value']})
        self.assertEqual(dic['data'], 'value')
        
    def test_findWithOneValueIndex(self):
        dic = MultiValueOneKeyDict({'data': ['value']})
        self.assertEqual(dic['data', 0], 'value')
        
    def test_findWithMultiValuesNoIndex(self):
        dic = MultiValueOneKeyDict({'data': ['value', 'value2']})
        self.assertEqual(dic['data'], ['value', 'value2'])
        
    def test_findWithMultiValuesIndex(self):
        dic = MultiValueOneKeyDict({'data': ['value', 'value2']})
        self.assertEqual(dic['data', 1], 'value2')
        
    def test_findWithMultiValueToManyArgs(self):
        with self.assertRaises(IndexError):
            dic = MultiValueOneKeyDict({'data': ['value', 'value2']})
            self.assertEqual(dic['data', 1, 3], 'value2')
            
    def test_getFindWithOneValueNoIndex(self):
        dic = MultiValueOneKeyDict({'data': ['value']})
        self.assertEqual(dic.get('data'), 'value')
        
    def test_getFindWithOneValueIndex(self):
        dic = MultiValueOneKeyDict({'data': ['value']})
        self.assertEqual(dic.get('data', 0), 'value')
        
    def test_getFindWithMultiValuesNoIndex(self):
        dic = MultiValueOneKeyDict({'data': ['value', 'value2']})
        self.assertEqual(dic.get('data'), ['value', 'value2'])
        
    def test_getFindWithMultiValuesIndex(self):
        dic = MultiValueOneKeyDict({'data': ['value', 'value2']})
        self.assertEqual(dic.get('data', 1), 'value2')
        
    def test_getWithDefualt(self):
        dic = MultiValueOneKeyDict({'data': ['value', 'value2']})
        self.assertEqual(dic.get('random', default='test'), 'test')
        
class SetTest(unittest.TestCase):
    def test_setStrNotInDict(self):
        dic = MultiValueOneKeyDict({'data': ['value']})
        dic['data2'] = 'value'
        self.assertEqual(dic._data, {'data': ['value'], 'data2': ['value']})
        
    def test_setListNotInDict(self):
        dic = MultiValueOneKeyDict({'data': ['value']})
        dic['data2'] = ['value', 'value2']
        self.assertEqual(dic._data, {'data': ['value'], 'data2': ['value', 'value2']})
        
    def test_setStrInDict(self):
        dic = MultiValueOneKeyDict({'data': ['value']})
        dic['data'] = 'value2'
        self.assertEqual(dic._data, {'data': ['value', 'value2']})
        
    def test_changeStrInDict(self):
        dic = MultiValueOneKeyDict({'data': ['value', 'value2']})
        dic['data', 1] = 'test'
        self.assertEqual(dic._data, {'data': ['value', 'test']})
        
    def test_indexProvidedButNotInDict(self):
        with self.assertRaises(IndexError):
            dic = MultiValueOneKeyDict({'data': ['value']})
            dic['data2', 1] = 'value2'
            
    def test_setDefaultValueExists(self):
        dic = MultiValueOneKeyDict({'data': ['value']})
        data = dic.setdefault('data')
        self.assertEqual(data, 'value')
        
    def test_setDefaultValueDoesntExist(self):
        dic = MultiValueOneKeyDict({'data': ['value']})
        data = dic.setdefault('data2', value='value3')
        self.assertEqual(dic['data2'], 'value3')
        
    def test_overwriteValue(self):
        dic = MultiValueOneKeyDict({'data': ['value'],'data2': 'value3'})
        dic['data2', None] = 'anotherValue'
        self.assertEqual(dic['data2'], 'anotherValue')
        
class DeleteTest(unittest.TestCase):
    def test_deleteKey(self):
        dic = MultiValueOneKeyDict({'data': ['value', 'value2']})
        del dic['data']
        self.assertEqual(dic._data, {})
        
    def test_deleteValueFromKey(self):
        dic = MultiValueOneKeyDict({'data': ['value', 'value2']})
        del dic['data', 1]
        self.assertEqual(dic._data, {'data': ['value']})
        
class MiscTest(unittest.TestCase):
    def test_keys(self):
        dic = MultiValueOneKeyDict({'data': ['value', 'value2']})
        self.assertEqual(list(dic.keys()), ['data'])
        
    def test_items(self):
        dic = MultiValueOneKeyDict({'data': ['value', 'value2']})
        self.assertEqual(list(dic.keys()), ['data'])
        
    def test_copy(self):
        dic = MultiValueOneKeyDict({'data': ['value', 'value2']})
        self.assertEqual(dic.copy(), {'data': ['value', 'value2']})