import ConfigParser
import unittest

import commands.translate as translate


class TestTorrent(unittest.TestCase):
    def test_translate(self):
        fullMessageText = 'trippy wirbel'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        translate.run(chatId, 'Admin', fullMessageText)
