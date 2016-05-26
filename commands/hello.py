import ConfigParser

import telegram


def run(chat_id, user, message):
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    bot.sendMessage(chat_id=chat_id, text='Wazzup')
