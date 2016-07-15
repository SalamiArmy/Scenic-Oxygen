import ConfigParser
import unittest
import telegram

import commands.get as get


class TestGet(unittest.TestCase):
    def test_get(self):
        requestText = 'dat boi'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        #for bot group:
        #chatId = -1001048076684

        get.run(bot, keyConfig, chatId, 'Admin', requestText)
