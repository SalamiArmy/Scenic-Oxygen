import ConfigParser

import sys
import unittest

import telegram

import commands.getfig as getfig


class TestGetFig(unittest.TestCase):
    def test_getfig(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        try:
            getfig.run(chatId, 'Admin', '')
