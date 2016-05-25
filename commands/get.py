import ConfigParser
import os

import http
import json
import string
import urllib
import random
import socket
import telegram


def run(thorin, update):
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(os.getenv("THORIN_API_TOKEN"))

    # chat_id is required to reply to any message
    chat_id = update.message.chat_id
    message = update.message.text
    user = update.message.from_user.username \
        if not update.message.from_user.username == '' \
        else update.message.from_user.first_name + (' ' + update.message.from_user.last_name) \
        if not update.message.from_user.last_name == '' \
        else ''

    message = message.replace(bot.name, "").strip()

    splitText = message.split(' ', 1)

    requestText = splitText[1] if ' ' in message else ''

    # Ashley: Added a try catch here-
    # For weird 'Unautherized' error when sending photos.
    # Keeps track of the last user to receive a chat action.
    # Satisfies pending chat actions with a message instead of a photo.
    try:
        googurl = 'https://www.googleapis.com/customsearch/v1'
        args = {'cx': keyConfig.get('Google', 'GCSE_SE_ID'),
                'key': keyConfig.get('Google', 'GCSE_APP_ID'),
                'searchType': "image",
                'safe': "off",
                'q': requestText,
                'searchType': "image"}
        realUrl = googurl + '?' + urllib.urlencode(args)
        data = json.load(urllib.urlopen(realUrl))
        if 'items' in data and len(data['items']) >= 9:
            imagelink = 'x-raw-image:///'
            offset = 0
            randint = random.randint(0, 9)
            while imagelink.startswith('x-raw-image:///') and \
                            offset < 10 and \
                            randint + offset < len(data['items']):
                imagelink = data['items'][randint + offset]['link']
                offset = offset+1
            if not imagelink.startswith('x-raw-image:///') and not imagelink == '':
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
                userWithCurrentChatAction = chat_id
                urlForCurrentChatAction = imagelink
                bot.sendPhoto(chat_id=userWithCurrentChatAction,
                              photo=urlForCurrentChatAction.encode('utf-8'),
                              caption=(user + ': ' if not user == '' else '') +
                                      string.capwords(requestText.encode('utf-8')) +
                                      (' ' + imagelink if len(imagelink) < 100 else ''))
            else:
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +\
                                                      ', I\'m afraid I can\'t find any images for ' +\
                                                      string.capwords(requestText.encode('utf-8')))
        else:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +\
                                                  ', I\'m afraid I can\'t find any images for ' +\
                                                  string.capwords(requestText.encode('utf-8')))
    except telegram.TelegramError or \
            socket.timeout or socket.error or \
            urllib.error.URLError or \
            http.client.BadStatusLine as e:
        adminGroupId = keyConfig['HeyBoet']['ADMIN_GROUP_CHAT_ID']
        if user != adminGroupId:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            return bot.sendMessage(chat_id=chat_id, text=requestText + ': ' + imagelink)
        if not adminGroupId == '':
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            return bot.sendMessage(chat_id=chat_id, text='Error: ' + e.message + '\n' +
                                                         'Request Text: ' + requestText + '\n' +
                                                         'Url: ' + imagelink)

