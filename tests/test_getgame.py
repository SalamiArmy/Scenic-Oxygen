import ConfigParser
import unittest

import telegram

import commands.getgame as getgame


class TestGetGame(unittest.TestCase):
    def test_getgame(self):
        requestText = 'infinite warfare'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        getgame.run(bot, keyConfig, chatId, 'Admin', requestText, 1)
