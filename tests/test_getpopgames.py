
import ConfigParser
import unittest

import telegram

from commands.getpopgames import run


class TestGetGame(unittest.TestCase):
    def test_getgame(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        run(bot, keyConfig, chatId, 'Admin')
