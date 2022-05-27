import unittest

from waffleweb.files import File

class FileTest(unittest.TestCase):
    def test_File(self):
        file = File('test.html', '<h1>Test Html</h1>', 'text/html', 18)
        self.assertEqual('<h1>Test Html</h1>', file.data)