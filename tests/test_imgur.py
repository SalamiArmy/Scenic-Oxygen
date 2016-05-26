import ConfigParser
import unittest

import commands.imgur as imgur


class TestImgur(unittest.TestCase):
    def test_imgur(self):
        fullMessageText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        imgur.run(chatId, 'Admin', fullMessageText)
