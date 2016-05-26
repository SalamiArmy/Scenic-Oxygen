import ConfigParser
import sys
import unittest

import telegram

import commands.define as define


class TestDefine(unittest.TestCase):
    def test_define(self):
        fullMessageText = '@Bashs_Bot define trippy'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        define.run(chatId, 'Admin', fullMessageText)
