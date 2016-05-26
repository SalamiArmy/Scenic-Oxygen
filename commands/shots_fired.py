import ConfigParser

import telegram


def run(chat_id, user, message):
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    try:
        target = message.split(" ")[message.split(" ").index("shots_fired") + 1]
        bot.sendMessage(chat_id=chat_id, text="pew PEW pew " + target + " PEW pew PEW")
    except:
        return "pew pew PEW PEW PEW"
