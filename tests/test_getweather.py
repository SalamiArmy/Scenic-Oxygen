import ConfigParser
import unittest

import commands.getweather as getweather


class TestGetWeather(unittest.TestCase):
    def test_getweather(self):
        fullMessageText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getweather.run(chatId, 'Admin', fullMessageText)
