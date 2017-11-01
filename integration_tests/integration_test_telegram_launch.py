# coding=utf-8
import commands.login as login
import ConfigParser
import unittest
import telegram
from google.appengine.ext import ndb
from google.appengine.ext import testbed

import main
from commands import add
from integration_tests import command_codes


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

    def integration_test_launch(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        add.setCommandCode('launch', command_codes.get_launch_code())
        launch = main.load_code_as_module('launch')
        launch.run(bot, chatId, 'Admin', keyConfig)

    def integration_test_post_launch(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        keyConfig.read(["keys.ini", "..\keys.ini"])
        newRequestObject = main.TelegramWebhookHandler()
        class Object(object):
            pass
        newRequestObject.request = Object()
        newRequestObject.request.body = '{"message": {"from": {"username": "SalamiArmy", "first_name": "Ashley", "last_name": "Lewis"}, "text": "/launch", "chat": {"id": ' + keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID') + ', "type": "group"}}}'
        newRequestObject.response = Object()
        newRequestObject.response.write = lambda x: None

        add.setCommandCode('launch', command_codes.get_launch_code())
        newRequestObject.post()
