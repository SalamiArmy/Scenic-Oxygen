import ConfigParser
import requests
import telegram


# http://api.funtranslations.com/translate/yoda.json?text=
def translate(msg):
    r = requests.get("http://api.funtranslations.com/translate/yoda.json?text=" + msg)
    if r.status_code == 429:
        return "Sorry I can only translate 5 times per hour"
    try:
        return r.json()['contents']['translated'].replace("  ", " ")
    except:
        print(r.text)
        return "An unexpected error occurred"

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    bot.sendMessage(chat_id=chat_id, text=(user + ": ") if user != '' else '' + translate(message))
    return True
