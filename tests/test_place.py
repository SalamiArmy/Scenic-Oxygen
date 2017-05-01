import ConfigParser
import unittest
import telegram

import commands.place as place


class TestPlace(unittest.TestCase):
    def test_place(self):
        requestText = 'Hillcrest'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        place.run(bot, chatId, 'Admin', keyConfig, requestText)
