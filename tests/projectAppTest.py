import unittest
from waffleweb import WaffleProject
from waffleweb.exceptions import AppNotFoundError

class projectAppTest(unittest.TestCase):
    def test_importPyAppValid(self):
        apps = [
            'testApp.py'
        ]

        try:
            proj = WaffleProject(apps)
        except AppNotFoundError:
            self.fail('App could not be found')

    def test_importPyAppInvalid(self):
        apps = [
            'apps.py'
        ]

        with self.assertRaises(AppNotFoundError):
            proj = WaffleProject(apps)

    def test_importFolderAppThatIsValid(self):
        apps = [
            'TestApp2'
        ]

        try:
            proj = WaffleProject(apps)
        except AppNotFoundError:
            self.fail('Could not find app')

    def test_importFolderAppThatDoesntExist(self):
        apps = [
            'appThatNone'
        ]

        with self.assertRaises(AppNotFoundError):
            proj = WaffleProject(apps)

    def test_importFolderWithoutPyFileInside(self):
        apps = [
            'TestApp3'
        ]

        with self.assertRaises(AppNotFoundError):
            proj = WaffleProject(apps)