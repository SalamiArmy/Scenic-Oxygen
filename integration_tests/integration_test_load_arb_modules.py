# coding=utf-8
import unittest
from google.appengine.ext import ndb
from google.appengine.ext import testbed

import commands.add as add
import command_codes

class TestModLoader_Unit(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_user_stub()
        # Clear ndb's in-context cache between telegram_tests.
        # This prevents data from leaking between telegram_tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()
        add.setCommandCode('HelloWorldMod', 'def run():\r\n    print \'Hello World\'')

    def test_mod_load(self):
        import main
        import HelloWorldMod
        HelloWorldMod.run()

    def test_perform_ndb_query(self):
        import main
        add.setCommandCode('retry_on_telegram_error', command_codes.retry_on_telegram_error_command_code())
        add.setCommandCode('get', command_codes.get_command_code())
        add.setCommandCode('getgif', command_codes.getgif_command_code())

        newRequestObject = main.TelegramWebhookHandler()
        class Object(object):
            pass
        newRequestObject.request = Object()
        newRequestObject.request.body = '{"message": {"from": {"username": "SalamiArmy", "first_name": "Ashley", "last_name": "Lewis"}, "text": "/getgif grade A 👌👌 100% 👌👌 good shit", "chat": {"id": -55348600, "type": "group"}}}'
        newRequestObject.response = Object()
        newRequestObject.response.write = lambda x: None
        newRequestObject.post()

