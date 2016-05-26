import ConfigParser
import unittest

import commands.getxxx as getxxx


class TestGetXXX(unittest.TestCase):
    def test_getxxx(self):
        fullMessageText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getxxx.run(chatId, 'Admin', fullMessageText)
