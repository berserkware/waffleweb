import unittest
from waffleweb.settings import getFromSettings

class BasicTests(unittest.TestCase):
    def test_FindObjectThatExistsNoDefualt(self):
        testItem = getFromSettings('TEST_ITEM')
        self.assertEqual(testItem, 'data')

    def test_FindObjectThatExistsDefualt(self):
        testItem = getFromSettings('TEST_ITEM', 'defualtValue')
        self.assertEqual(testItem, 'data')

    def test_FindObjectThatDoesntExistNoDefault(self):
        testItem = getFromSettings('DOESNT_EXIST')
        self.assertEqual(testItem, None)

    def test_FindOBjectThatDoesntExistDefualt(self):
        testItem = getFromSettings('DOESNT_EXIST', 'defualtValue')
        self.assertEqual(testItem, 'defualtValue')
