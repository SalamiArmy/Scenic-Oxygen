# coding=utf-8
import ConfigParser
import os

import telegram
import tungsten


#reverse image search imports:


def run(chat_id, user, message):
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    requestText = message.replace(bot.name, "").strip()


    client = tungsten.Tungsten(keyConfig.get('Wolfram', 'WOLF_APP_ID'))
    result = client.query(requestText)
    if len(result.pods) >= 1:
        fullAnswer = ''
        for pod in result.pods:
            for answer in pod.format['plaintext']:
                if not answer == None:
                    fullAnswer += answer.encode('ascii', 'ignore')
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = (user + ': ' if not user == '' else '') + fullAnswer
        bot.sendMessage(chat_id=chat_id, text=urlForCurrentChatAction)
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I can\'t find any answers for ' + \
                                  requestText.encode('utf-8')
        bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)