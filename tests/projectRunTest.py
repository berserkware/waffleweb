import unittest
from waffleweb import WaffleProject

class basicRunTest(unittest.TestCase):
    def test_checkIPInvalid(self):
        APPS = []

        project = WaffleProject(APPS)
        with self.assertRaises(ValueError):
            project.run('jsdf', 8000)
    
    def test_checkIPValid(self):
        APPS = []

        project = WaffleProject(APPS)
        try:
            project.run('127.0.0.1', 8000)
        except ValueError:
            self.fail('project.run() failed unexpectably!')

    def test_checkPortInvalid(self):
        APPS = []

        project = WaffleProject(APPS)
        with self.assertRaises(ValueError):
            project.run('127.0.0.1', 'hello')

    def test_checkPortInvalid1(self):
        APPS = []

        project = WaffleProject(APPS)
        with self.assertRaises(ValueError):
            project.run('127.0.0.1', -1)

    def test_checkPortInvalid2(self):
        APPS = []

        project = WaffleProject(APPS)
        with self.assertRaises(ValueError):
            project.run('127.0.0.1', 987654)

    def test_checkPortValid(self):
        APPS = []

        project = WaffleProject(APPS)
        try:
            project.run('127.0.0.1', 24474)
        except ValueError:
            raise ValueError('project.run() failed unexpectably!')