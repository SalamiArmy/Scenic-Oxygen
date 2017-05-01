import ConfigParser
import unittest
import telegram

from commands.getsound import run


class TestGetSound(unittest.TestCase):
    def test_getsound(self):
        requestText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        run(bot, chatId, 'Admin', keyConfig, requestText)
