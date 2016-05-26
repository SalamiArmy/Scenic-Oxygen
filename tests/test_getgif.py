import ConfigParser
import unittest

import commands.getgif as getgif


class TestGetGif(unittest.TestCase):
    def test_getgif(self):
        fullMessageText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgif.run(chatId, 'Admin', fullMessageText)
