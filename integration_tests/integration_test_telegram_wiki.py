# coding=utf-8
import ConfigParser
import unittest
import telegram
from google.appengine.ext import ndb
from google.appengine.ext import testbed

import main
from commands import add
from integration_tests import command_codes


class WikiIntegrationTests(unittest.TestCase):
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

    def integration_wiki_test(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        launch = main.load_command_module('wiki', command_codes.get_wiki_code())
        launch.run(bot, chatId, 'Admin', keyConfig, 'list of ongoing conflicts')

    def post_wiki_test(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        keyConfig.read(["keys.ini", "..\keys.ini"])
        newRequestObject = main.TelegramWebhookHandler()
        class Object(object):
            pass
        newRequestObject.request = Object()
        newRequestObject.request.body = '{"message": {"from": {"username": "SalamiArmy", "first_name": "Ashley", "last_name": "Lewis"}, "text": "/wiki list of ongoing conflicts", "chat": {"id": ' + keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID') + ', "type": "private"}}}'
        newRequestObject.response = Object()
        newRequestObject.response.write = lambda x: None

        add.setCommandCode('wiki', command_codes.get_wiki_code())
        newRequestObject.post()
