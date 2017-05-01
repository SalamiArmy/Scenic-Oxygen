import ConfigParser
import unittest

import telegram

import commands.define as define


class TestDefine(unittest.TestCase):
    def test_define(self):
        requestText = 'chicanes'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        define.run(bot, chatId, 'Admin', keyConfig, requestText)
