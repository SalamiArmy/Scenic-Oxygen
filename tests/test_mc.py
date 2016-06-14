import ConfigParser
import unittest
import telegram

import commands.mc as mc


class TestMC(unittest.TestCase):
    def test_mc(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        self.assertTrue(mc.run(bot, keyConfig, chatId, 'Admin', ''))
