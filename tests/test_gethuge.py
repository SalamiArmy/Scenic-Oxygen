import ConfigParser
import unittest
import telegram

import commands.gethuge as gethuge


class TestGetHuge(unittest.TestCase):
    def test_gethuge(self):
        requestText = 'it\'s a beautiful day to kill yourself'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        #chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        #for bot group:
        chatId = -1001048076684

        gethuge.run(bot, keyConfig, chatId, 'Admin', requestText)
