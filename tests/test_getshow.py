import ConfigParser
import unittest
import telegram

import commands.getshow as getshow


class TestGetShow(unittest.TestCase):
    def test_getshow(self):
        requestText = 'x-files'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'ADMIN_GROUP_CHAT_ID')

        getshow.run(bot, keyConfig, chatId, 'Admin', requestText)
