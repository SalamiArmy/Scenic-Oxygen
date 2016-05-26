import ConfigParser
import unittest

import commands.gethuge as gethuge


class TestGetHuge(unittest.TestCase):
    def test_gethuge(self):
        fullMessageText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        gethuge.run(chatId, 'Admin', fullMessageText)
