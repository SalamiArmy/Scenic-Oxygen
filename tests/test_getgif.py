import ConfigParser
import json
import unittest
import urllib

import telegram

import commands.getgif as getgif


class TestGetGif(unittest.TestCase):
    def test_getgif(self):
        requestText = 'coconut slaughter'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getgif.run(bot, chatId, 'Admin', keyConfig, requestText)