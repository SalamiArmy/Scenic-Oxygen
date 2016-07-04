import ConfigParser
import unittest
import telegram

import commands.giphy as giphy


class TestGiphy(unittest.TestCase):
    def test_giphy(self):
        requestText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        self.assertTrue(giphy.run(bot, keyConfig, chatId, 'Admin', requestText))
