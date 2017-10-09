# coding=utf-8
import importlib
import unittest
from google.appengine.ext import ndb
from google.appengine.ext import testbed

import main

class TestModLoader(unittest.TestCase):
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

    def integration_test_mod_load(self):
        newModLoaderObject = main.WebhookHandler()
        mod = newModLoaderObject.load_code_as_module('print \'Hello World\'', 'HelloWorldMod')
        mod = importlib.import_module('HelloWorldMod')
        mod