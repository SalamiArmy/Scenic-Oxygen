import ConfigParser
import unittest

import commands.gethugegif as gethugegif


class TestGetHugeGif(unittest.TestCase):
    def test_gethugegif(self):
        fullMessageText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        gethugegif.run(chatId, 'Admin', fullMessageText)
