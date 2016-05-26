import ConfigParser
import json
import random
import string
import sys
import urllib

import telegram


def run(chat_id, user, message):
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    requestText = message.replace(bot.name, "").strip()

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
                bot.sendPhoto(chat_id=chat_id,
                              photo=imagelink.encode('utf-8'),
                              caption=(user + ': ' if not user == '' else '') +
                                      string.capwords(requestText.encode('utf-8')) +
                                      (' ' + imagelink if len(imagelink) < 100 else '').encode('utf-8'))
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
    except:
        adminGroupId = keyConfig.get('HeyBoet', 'ADMIN_GROUP_CHAT_ID')
        if user != adminGroupId:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            bot.sendMessage(chat_id=chat_id, text=requestText + ': ' + imagelink)
        if adminGroupId:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            bot.sendMessage(chat_id=chat_id, text='Error: ' + str(sys.exc_info()[1]) + '\n' +
                                                  'Request Text: ' + requestText + '\n' +
                                                  'Url: ' + imagelink)

