import ConfigParser
import unittest
import telegram

import commands.launch as launch


class TestLaunch(unittest.TestCase):
    def test_launch(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        #for bot group:
        #chatId = -130436192

        launch.run(bot, chatId, 'Admin', keyConfig, '')
