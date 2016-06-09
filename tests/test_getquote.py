import ConfigParser
import unittest
import telegram

import commands.getquote as getquote


class TestGetQuote(unittest.TestCase):
    def test_getquote(self):
        requestText = 'no more hairy bush nuns'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getquote.run(bot, keyConfig, chatId, 'Admin', requestText)