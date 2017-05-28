# coding=utf-8
import ConfigParser
import unittest

import telegram

import commands.getgif as getgif
from google.appengine.ext import ndb
from google.appengine.ext import testbed

import main


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

    def test_getgif(self):
        requestText = 'grade A 👌👌 100% 👌👌 good shit'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        getgif.setPreviouslySeenGifsValue(chatId, '')
        getgif.run(bot, chatId, 'Admin', keyConfig, requestText, 1)

    def test_getgif_full(self):
        newRequestObject = main.WebhookHandler()
        class Object(object):
            pass
        newRequestObject.request = Object()
        newRequestObject.request.body = '{"message": {"from": {"username": "SalamiArmy", "first_name": "Ashley", "last_name": "Lewis"}, "text": "/getgif grade A 👌👌 100% 👌👌 good shit", "chat": {"id": -55348600, "type": "group"}}}'
        newRequestObject.response = Object()
        newRequestObject.response.write = lambda x: None
        newRequestObject.post()
