import ConfigParser
import sys
import unittest

import telegram

import commands.getanswer as getanswer


class TestGetAnswer(unittest.TestCase):
    def test_getanswer(self):
        fullMessageText = 'How long is a piece of string?'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        #for bot group:
        #chatId = -1001048076684

        getanswer.run(chatId, 'Admin', fullMessageText)
