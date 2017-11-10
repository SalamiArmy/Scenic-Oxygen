import ConfigParser
import unittest
import telegram

from commands import classicget

class TestAdd(unittest.TestCase):
    def test_add(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')
        classicget.run(bot, chatId)
