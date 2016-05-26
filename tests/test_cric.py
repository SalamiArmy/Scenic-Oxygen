import ConfigParser
import unittest

import commands.cric as cric


class TestCric(unittest.TestCase):
    def test_cric(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        cric.run(chatId, 'Admin', '')
