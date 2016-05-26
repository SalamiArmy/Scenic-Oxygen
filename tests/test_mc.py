import ConfigParser
import unittest

import commands.mc as mc


class TestMC(unittest.TestCase):
    def test_mc(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        mc.run(chatId, 'Admin', '')
