import ConfigParser
import unittest

import commands.getmovie as getmovie


class TestGetMovie(unittest.TestCase):
    def test_getmovie(self):
        fullMessageText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getmovie.run(chatId, 'Admin', fullMessageText)
