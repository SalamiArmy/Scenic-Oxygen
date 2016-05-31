import ConfigParser
import unittest

import telegram

import commands.getanswer as getanswer


class TestGetAnswer(unittest.TestCase):
    def test_getanswer(self):
        requestText = 'how many jupiters can fit in the sun?'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        #for bot group:
        #chatId = -1001048076684

        getanswer.run(bot, keyConfig, chatId, 'Admin', requestText)
