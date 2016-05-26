import ConfigParser
import unittest

import commands.iss as iss


class TestISS(unittest.TestCase):
    def test_iss(self):
        fullMessageText = 'Durban'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        iss.run(chatId, 'Admin', fullMessageText)

    def test_isspos(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        iss.run(chatId, 'Admin', '')
