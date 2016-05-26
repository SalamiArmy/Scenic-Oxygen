import ConfigParser
import unittest

import commands.place as place


class TestPlace(unittest.TestCase):
    def test_place(self):
        fullMessageText = 'Hillcrest'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        place.run(chatId, 'Admin', fullMessageText)
