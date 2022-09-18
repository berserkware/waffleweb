import unittest
from waffleweb.app import WaffleApp, app
from waffleweb.request import Request
from waffleweb.exceptions import AppNotFoundError, ViewNotFoundError
from waffleweb.template import getRelativeUrl, renderTemplate
import apps.testApp

class RenderTemplateTest(unittest.TestCase):
    def test_renderWithoutContext(self):
        res = renderTemplate('testWithoutContext.html')
        self.assertEqual('<h1>Testing Testing 1 2 3</h1>', res)

    def test_renderWithContext(self):
        res = renderTemplate('testWithContext.html', {'testVar': 'Testing 1 2 3'})
        self.assertEqual('<h1>Testing Testing 1 2 3</h1>', res)
class GetRelativeUrlTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_basicTest(self):
        #This sets the currentWorkingApp to find the relative URLs    
        app.request(b'GET / HTTP1/1')

        url = getRelativeUrl('BasicTest')
        self.assertEqual(url, 'BasicTest/')
    
    def test_noKwargs(self):
        #This sets the currentWorkingApp to find the relative URLs    
        app.request(b'GET / HTTP1/1')

        with self.assertRaises(KeyError):
            getRelativeUrl('WithArgsTest')
    
    def test_kwargsRight(self):
        #This sets the currentWorkingApp to find the relative URLs    
        app.request(b'GET / HTTP1/1')

        url = getRelativeUrl('WithArgsTest', testArg1='test1', testArg2='test2')
        self.assertEqual(url, '/WithArgsTest/test1/test/test2/')
    
    def test_notEnoughtKwargs(self):
        #This sets the currentWorkingApp to find the relative URLs    
        app.request(b'GET / HTTP1/1')

        with self.assertRaises(KeyError):
            getRelativeUrl('WithArgsTest', testArg1='test1')
    
    def test_ViewNotFound(self):
        #This sets the currentWorkingApp to find the relative URLs    
        app.request(b'GET / HTTP1/1')

        with self.assertRaises(ViewNotFoundError):
            getRelativeUrl('bolony')
            
    def test_inTemplate(self):
        #This sets the currentWorkingApp to find the relative URLs    
        app.request(b'GET / HTTP1/1')

        render = renderTemplate('inTemplateTest.html')
        self.assertEqual(render, 'BasicTest/')
    
