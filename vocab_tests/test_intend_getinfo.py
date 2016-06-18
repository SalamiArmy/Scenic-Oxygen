import ConfigParser
import unittest

import telegram

import vocabs


class TestIntentions(unittest.TestCase):
    def test_intend_getinfo_run_command_hierarchy(self):
        requestText = '@Bashs_Bot I asked you when will i ascend?'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        vocabs.intend_getinfo.run_command_hierarchy(bot, keyConfig, chatId, 'Admin', requestText, 50)