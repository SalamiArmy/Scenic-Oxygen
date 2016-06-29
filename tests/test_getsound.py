import ConfigParser
import unittest
import telegram

import commands.getsound as getsound


class TestGetSound(unittest.TestCase):
    def test_getsound(self):
        requestText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getsound.run(bot, keyConfig, chatId, 'Admin', requestText)
