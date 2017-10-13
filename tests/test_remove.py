import ConfigParser
import unittest
import telegram

import commands.remove as remove
import commands.add as add
import integration_tests.command_codes as command_codes
import main
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class TestRemove(unittest.TestCase):
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

    def test_remove(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')
        repo_url = keyConfig.get('GitHub', 'TESTING_GITHUB_USERNAME') + '/' + keyConfig.get('GitHub', 'TESTING_GITHUB_REPO')
        token_value = keyConfig.get('GitHub', 'TESTING_GITHUB_TOKEN')
        request_text = keyConfig.get('GitHub', 'TESTING_GITHUB_USERNAME') + ' ' + \
                       keyConfig.get('GitHub', 'TESTING_GITHUB_REPO') + ' ' + token_value

        add.setCommandCode('retry_on_telegram_error', command_codes.retry_on_telegram_error_command_code())
        add.setCommandCode('get', command_codes.get_command_code())
        add.setCommandCode('getgif', command_codes.getgif_command_code())

        add.setTokenValue(repo_url, token_value)

        remove.run(bot, chatId, 'Admin', keyConfig, request_text)

        self.assertEquals(add.getTokenValue(repo_url), '')
        self.assertEquals(main.load_code_as_module('retry_on_telegram_error'), None)
        self.assertEquals(main.load_code_as_module('get'), None)
        self.assertEquals(main.load_code_as_module('getgif'), None)

    def test_RemoveHook(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')
        result = remove.remove_hook(bot, chatId, keyConfig, keyConfig.get('GitHub', 'TESTING_GITHUB_USERNAME') + '/' + keyConfig.get('GitHub', 'TESTING_GITHUB_REPO'), keyConfig.get('GitHub', 'TESTING_GITHUB_TOKEN'))
        self.assertNotEqual(result,'')

    def test_RemoveCommands(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        repo_url = keyConfig.get('GitHub', 'TESTING_GITHUB_USERNAME') + '/' + keyConfig.get('GitHub', 'TESTING_GITHUB_REPO')
        token_value = keyConfig.get('GitHub', 'TESTING_GITHUB_TOKEN')

        add.setCommandCode('retry_on_telegram_error', command_codes.retry_on_telegram_error_command_code())
        add.setCommandCode('get', command_codes.get_command_code())
        add.setCommandCode('getgif', command_codes.getgif_command_code())

        remove.remove_commands(repo_url, token_value)
        self.assertEquals(main.load_code_as_module('retry_on_telegram_error'), None)
        self.assertEquals(main.load_code_as_module('get'), None)
        self.assertEquals(main.load_code_as_module('getgif'), None)
