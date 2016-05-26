import ConfigParser
import unittest

import commands.getshow as getshow


class TestGetShow(unittest.TestCase):
    def test_getshow(self):
        fullMessageText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getshow.run(chatId, 'Admin', fullMessageText)
