import ConfigParser
import unittest
import telegram

import commands.urban as urban


class TestUrban(unittest.TestCase):
    def test_urban(self):
        requestText = 'alsatian cannon'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        #for bot group:
        #chatId = -1001048076684

        urban.run(bot, chatId, 'Admin', keyConfig, requestText)
