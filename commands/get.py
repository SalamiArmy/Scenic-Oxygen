import ConfigParser
import telegram
import urllib
import urllib2
import random
import string
import json
import httplib
import socket


def run(thorin, incoming):
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read("commands/get.ini")
    
    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
    
    # chat_id is required to reply to any message
    chat_id = incoming.message.chat_id
    message = incoming.message.text
    user = incoming.message.from_user.username \
        if not incoming.message.from_user.username == '' \
        else incoming.message.from_user.first_name + (' ' + incoming.message.from_user.last_name) \
            if not incoming.message.from_user.last_name == '' \
            else ''

    splitText = message.split(bot.name + " ", 1)
    requestText = filter(lambda x: x in string.printable, splitText[1]) if ' ' in message else ''
    
    # Ashley: Added a try catch here-
    # For weird 'Unautherized' error when sending photos.
    # Keeps track of the last user to receive a chat action.
    # Satisfies pending chat actions with a message instead of a photo.
    userWithCurrentChatAction = ''
    urlForCurrentChatAction = ''
    requestTextForCurrentChatAction = ''
    googurl = 'https://www.googleapis.com/customsearch/v1'
    args = {'cx': keyConfig.get('Google', 'GCSE_SE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': "image",
            'safe': "off",
            'q': requestText}
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
            return imagelink
    return 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
                              ', I\'m afraid I can\'t find any images for ' +\
                              string.capwords(requestText.encode('utf-8'))