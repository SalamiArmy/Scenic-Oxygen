import ConfigParser
import unittest

import commands.getlyrics as getlyrics


class TestGetLyrics(unittest.TestCase):
    def test_getlyrics(self):
        fullMessageText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getlyrics.run(chatId, 'Admin', fullMessageText)
