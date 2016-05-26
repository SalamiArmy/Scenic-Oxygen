import ConfigParser
import unittest

import commands.reverseimage as reverseimage


class TestReverseImage(unittest.TestCase):
    def test_reverseimage(self):
        fullMessageText = 'http://i493.photobucket.com/albums/rr292/ReidxCore/PlainSwirl.jpg'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        reverseimage.run(chatId, 'Admin', fullMessageText)
