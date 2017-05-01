import ConfigParser
import unittest
import telegram

import commands.getlink as getlink


class TestGet(unittest.TestCase):
    def test_get(self):
        requestText = 'steam dev days'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        #for bot group:
        #chatId = -130436192

        getlink.run(bot, chatId, 'SalamiArmy', keyConfig, requestText)
