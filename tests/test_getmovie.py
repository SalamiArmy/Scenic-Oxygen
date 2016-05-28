import ConfigParser
import unittest
import telegram

import commands.getmovie as getmovie


class TestGetMovie(unittest.TestCase):
    def test_getmovie(self):
        requestText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getmovie.run(bot, keyConfig, chatId, 'Admin', requestText)
