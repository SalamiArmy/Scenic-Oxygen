import ConfigParser
import unittest
import telegram

import commands.gethuge as gethuge


class TestGetHuge(unittest.TestCase):
    def test_gethuge(self):
        requestText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        gethuge.run(bot, chatId, 'Admin', keyConfig, requestText)
