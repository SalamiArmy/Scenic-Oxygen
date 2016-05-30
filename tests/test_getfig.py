import ConfigParser

import sys
import unittest
import telegram

import telegram

import commands.getfig as getfig


class TestGetFig(unittest.TestCase):
    def test_getfig(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        try:
            getfig.run(bot, keyConfig, chatId, 'Admin', '')
