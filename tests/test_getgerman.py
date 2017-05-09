import ConfigParser
import unittest
import telegram

import commands.getgerman as getgerman


class TestTorrent(unittest.TestCase):
    def test_translate(self):
        requestText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        getgerman.run(bot, chatId, 'Admin', keyConfig, requestText)
