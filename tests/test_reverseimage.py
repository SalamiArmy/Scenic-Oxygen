import ConfigParser
import unittest
import telegram

import commands.reverseimage as reverseimage


class TestReverseImage(unittest.TestCase):
    def test_reverseimage(self):
        requestText = 'http://cdn.skim.gs/images/v1/msi/bt7jpt3wd6djuwc4rdn1/women-banned-from-instagram-for-being-too-hairy-down-there'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

        #for admin group
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        #for bot group:
        #chatId = -130436192

        #for personal chat
        #chatId = 33166369

        reverseimage.run(bot, keyConfig, chatId, 'Admin', requestText)
