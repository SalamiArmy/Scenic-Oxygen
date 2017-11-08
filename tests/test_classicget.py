from google.cloud import logging
import ConfigParser
import unittest
import telegram

import commands.add as add

class TestAdd(unittest.TestCase):
    def test_add(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')
        request_text = keyConfig.get('GitHub', 'TESTING_GITHUB_USERNAME') + ' ' + \
                       keyConfig.get('GitHub', 'TESTING_GITHUB_REPO') + ' ' + \
                       keyConfig.get('GitHub', 'TESTING_GITHUB_TOKEN')
        client = logging.Client(project='scenic-oxygen-113812', credentials=)
        print client.list_entries()[0]
