import ConfigParser
import unittest

import telegram

import commands.getgame as getgame


class TestGetGame(unittest.TestCase):
    def test_getgame(self):
        requestText = 'SUPERHOT'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgame.run(bot, keyConfig, chatId, 'Admin', requestText)
