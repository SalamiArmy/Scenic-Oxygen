import ConfigParser
import unittest

import telegram

import commands.gw2timers as gw2timers


class TestGetGame(unittest.TestCase):
    def test_getgame(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        gw2timers.run(bot, chatId, 'Admin', keyConfig)
