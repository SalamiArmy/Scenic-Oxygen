# coding=utf-8
import commands.login as login
import ConfigParser
import unittest
import telegram
from google.appengine.ext import ndb
from google.appengine.ext import testbed

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
        # Clear ndb's in-context cache between telegram_tests.
        # This prevents data from leaking between telegram_tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def integration_test_login(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        login.run(bot, chatId, 'Admin', keyConfig, 'ee4a')
        login.setPin(chatId, 'ee4a')
        login.run(bot, chatId, 'Admin', keyConfig, 'ee4a')
