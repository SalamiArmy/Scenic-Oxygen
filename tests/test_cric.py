import ConfigParser
import unittest
import telegram

import commands.cric as cric


class TestCric(unittest.TestCase):
    def test_cric(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        cric.run(bot, keyConfig, chatId, 'Admin', '')
