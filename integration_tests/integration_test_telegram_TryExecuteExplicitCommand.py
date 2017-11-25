# coding=utf-8
import ConfigParser
import unittest
from google.appengine.ext import ndb
from google.appengine.ext import testbed
import commands.add as add
import command_codes

import main

class TestPost(unittest.TestCase):
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
        add.setCommandCode('get', command_codes.getgif_command_code())
        add.setCommandCode('getgif', command_codes.get_command_code())

    def integration_test_post(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        keyConfig.read(["keys.ini", "..\keys.ini"])
        newRequestObject = main.TelegramWebhookHandler()
        class Object(object):
            pass
        newRequestObject.request = Object()
        newRequestObject.response = Object()
        newRequestObject.response.write = lambda x: None
        newRequestObject.TryExecuteExplicitCommand(keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID'), 'Admin', '/get commando', 'private' )
