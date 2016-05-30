import random
import ConfigParser


def choose(msg):
    split = msg.split(" ")
    return split[random.randrange(0, len(split))]

def run(bot, keyConfig, chat_id, user, message):
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    bot.sendMessage(chat_id=chat_id, text=choose(message))
