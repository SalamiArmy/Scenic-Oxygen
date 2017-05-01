import ConfigParser
import unittest
import telegram

import commands.imgur as imgur


class TestImgur(unittest.TestCase):
    def test_imgur(self):
        requestText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        imgur.run(bot, chatId, 'Admin', keyConfig, requestText)
