import ConfigParser
import sys
import unittest

import telegram

import commands.getbook as getbook


class TestGetBook(unittest.TestCase):
    def test_getbook(self):
        fullMessageText = 'trippy swirl'
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        #for bot group:
        #chatId = -1001048076684

        getbook.run(chatId, 'Admin', fullMessageText)
