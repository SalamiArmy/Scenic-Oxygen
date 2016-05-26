import ConfigParser
import sys
import unittest

import telegram

import commands.bitcoin as bitcoin


class TestBitcoin(unittest.TestCase):
    def test_bitcoin(self):
        fullMessageText = '@Bashs_Bot bitcoin'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        bitcoin.run(chatId, 'Admin', fullMessageText)
