import ConfigParser
import unittest

import telegram

import commands.watchgif as watchgif
#from commands.watchgif import run
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
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def test_watchgif(self):
        requestText = 'dog balls jiggle physics'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        #bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        #chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        watchgif.setWatchValue(0, '', 'myval')
        watchgif.addPreviouslyAddedLinkValue(0, '', 'mysecondval')
        watchgif.getWatchValue(0, '')
        #run(bot, chatId, 'SalamiArmy', keyConfig, requestText)
