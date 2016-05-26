import ConfigParser
import sys
import unittest

import telegram

import commands.rand as rand


class TestRand(unittest.TestCase):
    def test_rand(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        rand.run(chatId, 'Admin', '')
