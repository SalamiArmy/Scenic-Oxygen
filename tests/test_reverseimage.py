import ConfigParser
import unittest
import telegram

import commands.reverseimage as reverseimage


class TestReverseImage(unittest.TestCase):
    def test_reverseimage(self):
        requestText = 'https://media.giphy.com/media/11VleI37LdnKEw/giphy.gif'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        #chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        #for bot group:
        chatId = -130436192

        reverseimage.run(bot, keyConfig, chatId, 'Admin', requestText)
