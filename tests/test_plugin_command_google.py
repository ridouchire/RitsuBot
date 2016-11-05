# -*-coding:utf-8 -*-
import os, sys
sys.path.append(os.path.abspath(os.path.curdir))
from plugin_command_google import *
from common import *
from ritsu_config import PROXY

import unittest
from wsgiref.simple_server import make_server
import threading

host = 'localhost'
port = '8000'
path = '/search'
query = 'q=python'
se = None
def test_server(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', "text/html; charset=utf-8")]
    start_response(status, headers)
    if environ['HTTP_HOST'] == host + ':' + port and \
       environ['SERVER_PORT'] == port and \
       environ['PATH_INFO'] == path and \
       environ['QUERY_STRING'] == query:
        return [open('tests/{}.python.html'.format(se)).read()]
    else:
        return ['Failed!']

httpd = make_server(host, int(port), test_server)
print("Serving on port {}...".format(port))

class GetSearchPageTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        global httpd
        self.httpd = httpd
        self.bot = Bot(room, nick)
        self.url = 'http://{}:{}{}?{}'.format(host, port, path, query)
        
    def setUp(self):
        self.server = threading.Thread(target=self.httpd.handle_request, args=(), kwargs={})
        self.server.start()

    @unittest.skipIf(PROXY['ENABLED'],
                     "not supported through proxy")
    def test_get_search_page_google(self):
        global se
        se = 'google'
        print('\nURL: {}, using "{}" search engine'.format(self.url, se))
        self.assertEqual(
            get_search_page('python', se, self.url),
            open('tests/{}.python.html'.format(se)).read()
        )

    @unittest.skipIf(PROXY['ENABLED'],
                     "not supported through proxy")
    def test_get_search_page_sputnik(self):
        global se
        se = 'sputnik'
        print('\nURL: {}, using "{}" search engine'.format(self.url, se))
        self.assertEqual(
            get_search_page('python', se, self.url),
            open('tests/{}.python.html'.format(se)).read()
        )
    

class GetLinksTestCase(unittest.TestCase):
    links = {
        'google': [
            'https://www.python.org/',
            'https://en.wikipedia.org/wiki/Python_(programming_language)',
            'https://www.reddit.com/r/Python/',
            'http://planetpython.org/',
            'https://xkcd.com/353/',
            'https://www.tutorialspoint.com/python/',
            'https://www.codecademy.com/learn/python'
        ],
        'sputnik': [
            'https://ru.wikipedia.org/wiki/Python',
            'https://www.python.org/about/',
            'http://en.wikipedia.org/wiki/Python_%28programming_language%29',
            'http://python-3.ru/',
            'https://habrahabr.ru/hub/python/',
            'https://ru.wikibooks.org/wiki/Python',
            'http://www.onlamp.com/python/',
            'http://www.activestate.com/activepython',
            'http://pep8.ru/',
            'http://python.su/'
        ]
    }
    
    def test_get_links(self):
        for se in ['google', 'sputnik']:
            self.assertEqual(
                get_links(open('tests/{}.python.html'.format(se)).read(), se),
                self.links[se]
            )    

 
class CommandSearchTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.bot = Bot(room, nick)
        load(self.bot)
    def test_command_search(self):
        message = Message()
        for se in ['google', 'sputnik']:
            self.assertRegexpMatches(
                get_search_function(se)(self.bot, room, 'nick1', '', 'python', message),
                r'^http[s]?://.*[\.]+[\w]*/.*$'
            )
            self.assertNotEqual(
                get_search_function(se)(self.bot, room, 'nick1', '', 'python', message),
                get_search_function(se)(self.bot, room, 'nick1', '', 'python', message)
            )
            self.assertRegexpMatches(
                get_search_function(se)(self.bot, room, 'nick1', '', '', message),
                r'^http[s]?://.*[\.]+[\w]*/.*$'
            )
            self.assertEqual(
                get_search_function(se)(self.bot, room, 'nick2', '', '', message),
                'Query expected.'
            )
            self.assertRegexpMatches(
                get_search_function(se)(self.bot, room, 'nick2', '', 'haskell', message),
                r'^http[s]?://.*[\.]+[\w]*/.*$'
            )
            self.bot.ss[se]['current'] = len(self.bot.ss[se]['links']) -1
            self.assertEqual(
                get_search_function(se)(self.bot, room, 'nick2', '', '', message),
                'End of search results. Please refine your search query.'
            )
            self.assertEqual(
                get_search_function(se)(self.bot, room, 'nick1', '', '', message),
                'Query expected.'
            )
            
            
    
if __name__ == "__main__":
    get_search_page_suite = unittest.TestLoader().loadTestsFromTestCase(GetSearchPageTestCase)
    get_links_suite = unittest.TestLoader().loadTestsFromTestCase(GetLinksTestCase)
    command_search_suite = unittest.TestLoader().loadTestsFromTestCase(CommandSearchTestCase)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(get_search_page_suite)
    runner.run(get_links_suite)
    runner.run(command_search_suite)
    #unittest.main()
