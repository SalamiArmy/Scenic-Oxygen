import ConfigParser
import unittest
import telegram

import commands.add as add
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class TestAdd(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_user_stub()
        self.testbed.init_urlfetch_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def test_add(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')
        request_text = keyConfig.get('GitHub', 'TESTING_GITHUB_USERNAME') + ' ' + \
                       keyConfig.get('GitHub', 'TESTING_GITHUB_REPO') + ' ' + \
                       keyConfig.get('GitHub', 'TESTING_GITHUB_TOKEN')

        add.run(bot, chatId, 'Admin', keyConfig, request_text)

        self.assertEquals(add.getTokenValue(keyConfig, keyConfig.get('GitHub', 'TESTING_GITHUB_USERNAME') + '/' +
                                            keyConfig.get('GitHub', 'TESTING_GITHUB_REPO')), keyConfig.get('GitHub', 'TESTING_GITHUB_TOKEN'))

    def test_token_value_store(self):
        expectValue = 'garbled'
        add.setTokenValue('username/reponame', expectValue)
        self.assertEqual(add.getTokenValue('username/reponame'), expectValue)

    def test_add_CreateHook(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')
        add.create_hook(bot, chatId, keyConfig, keyConfig.get('GitHub', 'TESTING_GITHUB_USERNAME') + '/' + keyConfig.get('GitHub', 'TESTING_GITHUB_REPO'), keyConfig.get('GitHub', 'TESTING_GITHUB_TOKEN'))