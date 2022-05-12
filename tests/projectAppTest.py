import unittest

from waffleweb import WaffleProject
from waffleweb.project import AppNotFoundError, AppImportError

class projectAppTest(unittest.TestCase):
    def test_importPyAppValid(self):
        apps = [
            'testApp.app'
        ]

        try:
            proj = WaffleProject(apps)
        except AppNotFoundError:
            self.fail('App could not be found')

    def test_importPyAppInvalid(self):
        apps = [
            'apps'
        ]

        with self.assertRaises(AppImportError):
            proj = WaffleProject(apps)

    def test_importFolderAppThatIsValid(self):
        apps = [
            'TestApp2.app'
        ]

        try:
            proj = WaffleProject(apps)
        except AppNotFoundError:
            self.fail('Could not find app')

    def test_importFolderAppThatDoesntExist(self):
        apps = [
            'appThatNone.app'
        ]

        with self.assertRaises(AppNotFoundError):
            proj = WaffleProject(apps)

    def test_importFolderWithoutPyFileInside(self):
        apps = [
            'TestApp3.app'
        ]

        with self.assertRaises(AppNotFoundError):
            proj = WaffleProject(apps)