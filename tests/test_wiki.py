import ConfigParser
import unittest
import telegram

import commands.wiki as wiki


class TestWiki(unittest.TestCase):
    def test_wiki(self):
        requestText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        wiki.run(bot, keyConfig, chatId, 'Admin', requestText)
