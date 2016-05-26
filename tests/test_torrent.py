import ConfigParser
import unittest

import commands.torrent as torrent


class TestTorrent(unittest.TestCase):
    def test_torrent(self):
        fullMessageText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        torrent.run(chatId, 'Admin', fullMessageText)
