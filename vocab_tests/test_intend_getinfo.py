import ConfigParser
import unittest

import telegram

import vocabs


class TestIntentions(unittest.TestCase):
    def test_intend_getinfo_run_command_hierarchy(self):
        requestText = 'How big is the sun?'
        WhoWhatHow = 'the sun?'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        #chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        #for bot group:
        chatId = -1001048076684

        vocabs.intend_getinfo.run_command_hierarchy(bot, keyConfig, chatId, 'Admin', requestText, WhoWhatHow, 50)