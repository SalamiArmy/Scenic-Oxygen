import ConfigParser
import unittest

import commands.launch as launch


class TestLaunch(unittest.TestCase):
    def test_launch(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        launch.run(chatId, 'Admin', '')
