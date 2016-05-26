# coding=utf-8
import ConfigParser
import os

import soundcloud
import telegram


#reverse image search imports:


def run(chat_id, user, message):
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    requestText = message.replace(bot.name, "").strip()


    client = soundcloud.Client(client_id=keyConfig.get('Soundcloud', 'SC_CLIENT_ID'))
    track = client.get('/tracks', q=requestText.encode('utf-8'), sharing='public')
    if len(track) >= 1:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = (user + ': ' if not user == '' else '') + \
                                  track[0].permalink_url
        bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I can\'t find the sound of ' + \
                                  requestText.encode('utf-8') + '.'
        bot.sendMessage(chat_id=chat_id, text=urlForCurrentChatAction)