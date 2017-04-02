import ConfigParser
import sys
import unittest
import telegram

import telegram

import commands.getbook as getbook


class TestGetBook(unittest.TestCase):
    def test_getbook(self):
        requestText = 'four roads cross'
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        #for bot group:
        #chatId = -1001048076684

        getbook.run(bot, chatId, 'Admin', keyConfig, requestText)
