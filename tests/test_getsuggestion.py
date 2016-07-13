import ConfigParser
import unittest
import telegram

import commands.getsuggestion as getsuggestion


class TestGet(unittest.TestCase):
    def test_get(self):
        requestText = 'pokemon g'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        #for bot group:
        #chatId = -1001048076684

        getsuggestion.run(bot, keyConfig, chatId, 'Admin', requestText)
