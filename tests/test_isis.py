import ConfigParser
import unittest
import telegram

import commands.isis as isis


class TestISIS(unittest.TestCase):
    def test_isis(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        isis.run(bot, chatId, 'Admin', keyConfig, '')
