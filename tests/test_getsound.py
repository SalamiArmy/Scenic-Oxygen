import ConfigParser
import unittest

import commands.getsound as getsound


class TestGetSound(unittest.TestCase):
    def test_getsound(self):
        fullMessageText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getsound.run(chatId, 'Admin', fullMessageText)
