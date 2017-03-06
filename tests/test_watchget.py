import ConfigParser
import unittest

import telegram

import commands.watch as watch


class TestGet(unittest.TestCase):
    def test_get(self):
        requestText = 'steam dev days'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        #chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        #for bot group:
        chatId = -130436192

        watch.run(bot, keyConfig, chatId, 'SalamiArmy', requestText)
