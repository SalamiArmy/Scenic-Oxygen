import ConfigParser
import unittest
import telegram

import commands.getweather as getweather


class TestGetWeather(unittest.TestCase):
    def test_getweather(self):
        requestText = 'coffee bay'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        getweather.run(bot, chatId, 'Admin', keyConfig, requestText)
