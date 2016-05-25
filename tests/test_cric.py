import ConfigParser
import sys
import unittest

import telegram

import commands.cric as cric


class TestCric(unittest.TestCase):
    def test_cric(self):
        fullMessageText = '@Bashs_Bot cric trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        chatId = keyConfig.get('HeyBoet', 'ADMIN_GROUP_CHAT_ID')

        #for bot group:
        #chatId = -1001048076684

        from_user = telegram.user.User(33166369, 'Ashley', last_name='Lewis', username='SalamiArmy')

        chat = telegram.chat.Chat(chatId, 'group', title='Admin Group')

        incomingMessage = telegram.message.Message(0, from_user, 1463933563, chat, text=fullMessageText, entities=[{'type': 'bot_command', 'offset': 0, 'length': 4}])

        incomingUpdate = telegram.update.Update(0, message=incomingMessage,)

        try:
            cric.run(None, incomingUpdate)
        except:
            self.assertTrue(False, str(sys.exc_info()[0]))
