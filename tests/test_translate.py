import ConfigParser
import unittest
import telegram

import commands.translate as translate


class TestTorrent(unittest.TestCase):
    def test_translate(self):
        requestText = 'trippy wirbel'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        translate.run(bot, keyConfig, chatId, 'Admin', requestText)
