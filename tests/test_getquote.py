import ConfigParser
import unittest

import commands.getquote as getquote


class TestGetQuote(unittest.TestCase):
    def test_getquote(self):
        fullMessageText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getquote.run(chatId, 'Admin', fullMessageText)
