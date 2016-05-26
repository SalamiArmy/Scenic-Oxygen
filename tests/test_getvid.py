import ConfigParser
import unittest

import commands.getvid as getvid


class TestGetVid(unittest.TestCase):
    def test_getvid(self):
        fullMessageText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getvid.run(chatId, 'Admin', fullMessageText)
