import ConfigParser
import sys
import unittest

import telegram

import commands.getgame as getgame


class TestGetGame(unittest.TestCase):
    def test_getgame(self):
        fullMessageText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgame.run(chatId, 'Admin', fullMessageText)
