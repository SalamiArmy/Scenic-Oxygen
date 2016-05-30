import ConfigParser
import unittest
import telegram

import commands.reverseimage as reverseimage


class TestReverseImage(unittest.TestCase):
    def test_reverseimage(self):
        requestText = 'http://i493.photobucket.com/albums/rr292/ReidxCore/PlainSwirl.jpg'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        reverseimage.run(bot, keyConfig, chatId, 'Admin', requestText)
