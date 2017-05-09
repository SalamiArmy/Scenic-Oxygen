import ConfigParser
import unittest
import telegram

import commands.torrent as torrent


class TestTorrent(unittest.TestCase):
    def test_torrent(self):
        requestText = 'athf'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        torrent.run(bot, chatId, 'Admin', keyConfig, requestText)
