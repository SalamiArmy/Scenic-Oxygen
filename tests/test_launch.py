import ConfigParser
import unittest
import telegram

import commands.launch as launch


class TestLaunch(unittest.TestCase):
    def test_launch(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        self.assertTrue(launch.run(bot, keyConfig, chatId, 'Admin', ''))
