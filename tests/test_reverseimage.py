import ConfigParser
import unittest
import telegram

import commands.reverseimage as reverseimage


class TestReverseImage(unittest.TestCase):
    def test_reverseimage(self):
        requestText = 'https://i.kinja-img.com/gawker-media/image/upload/t_original/jvv7ixccfzr1sueeed5f.gif'

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
