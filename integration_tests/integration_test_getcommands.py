# coding=utf-8
import unittest
from google.appengine.ext import ndb
from google.appengine.ext import testbed

import commands.add as add
import command_codes

class TestGet(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_user_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()
        add.setCommandCode('retry_on_telegram_error', command_codes.retry_on_telegram_error_command_code())
        add.setCommandCode('get', command_codes.get_command_code())
        add.setCommandCode('getgif', command_codes.getgif_command_code())

    def integration_test_get(self):
        import main
        newRequestObject = main.GetCommandsHandler()
        class Object(object):
            pass
        newRequestObject.response = Object()
        newRequestObject.response.write = lambda x: self.mockResponseWriter(x)
        self.responseString = ''
        newRequestObject.get()
        if self.responseString == '':
            raise Exception

    global responseString

    def mockResponseWriter(self, inputText):
        self.responseString = inputText
        return inputText