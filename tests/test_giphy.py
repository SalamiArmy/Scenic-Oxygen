import ConfigParser
import unittest

import commands.giphy as giphy


class TestGiphy(unittest.TestCase):
    def test_giphy(self):
        fullMessageText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        giphy.run(chatId, 'Admin', fullMessageText)
