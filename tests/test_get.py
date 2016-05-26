import ConfigParser
import sys
import unittest

import telegram

import commands.get as get


class TestGet(unittest.TestCase):
    def test_get(self):
        fullMessageText = '/get alsation cannon'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('HeyBoet', 'ADMIN_GROUP_CHAT_ID')

        #for bot group:
        #chatId = -1001048076684

        get.run(chatId, 'SalamiArmy', fullMessageText)
