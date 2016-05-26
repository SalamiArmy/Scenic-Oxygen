import ConfigParser
import unittest

import commands.isis as isis


class TestISIS(unittest.TestCase):
    def test_isis(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        isis.run(chatId, 'Admin', '')
