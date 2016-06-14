import ConfigParser
import sys
import unittest
import telegram

import telegram

import commands.rand as rand


class TestRand(unittest.TestCase):
    def test_rand(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        self.assertTrue(rand.run(bot, keyConfig, chatId, 'Admin', ''))
