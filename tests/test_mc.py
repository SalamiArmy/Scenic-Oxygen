import ConfigParser
import unittest
import telegram

import commands.mc as mc


class TestMC(unittest.TestCase):
    def test_mc(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        mc.run(bot, chatId, 'Admin', keyConfig, '')
