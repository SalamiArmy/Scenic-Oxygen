import ConfigParser
import unittest

import commands.wiki as wiki


class TestWiki(unittest.TestCase):
    def test_wiki(self):
        fullMessageText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        wiki.run(chatId, 'Admin', fullMessageText)
