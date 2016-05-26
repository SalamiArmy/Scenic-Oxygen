import ConfigParser
import unittest

import commands.urban as urban


class TestUrban(unittest.TestCase):
    def test_urban(self):
        fullMessageText = 'alsatian cannon'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        #for bot group:
        #chatId = -1001048076684

        urban.run(chatId, 'Admin', fullMessageText)
