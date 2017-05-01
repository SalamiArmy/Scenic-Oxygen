import ConfigParser
import unittest
import telegram

import commands.getvid as getvid


class TestGetVid(unittest.TestCase):
    def test_getvid(self):
        requestText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        getvid.run(bot, chatId, 'Admin', keyConfig, requestText)
