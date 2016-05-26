# coding=utf-8
import ConfigParser
import os
import urllib

import telegram
import json


def run(chat_id, user, message):
    # Read keys.ini file should be at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    requestText = message.replace(bot.name, "").strip()

    booksUrl = 'https://www.googleapis.com/books/v1/volumes?maxResults=1&key=' + \
               keyConfig.get('Google', 'GCSE_APP_ID') + '&q='
    realUrl = booksUrl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    if 'totalItems' in data and data['totalItems'] >= 1:
        bookData = data['items'][0]['volumeInfo']
        googleBooksUrl = data['items'][0]['accessInfo']['webReaderLink']
        if 'imageLinks' in bookData:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            userWithCurrentChatAction = chat_id
            urlForCurrentChatAction = 'Photo= ' + bookData['imageLinks']['thumbnail'] + \
                                      ' Caption= ' + (user + ': ' if not user == '' else '') + googleBooksUrl
            bot.sendPhoto(chat_id=userWithCurrentChatAction, photo=bookData['imageLinks']['thumbnail'],
                          caption=(user + ': ' if not user == '' else '') + googleBooksUrl)
        else:
            userWithCurrentChatAction = chat_id
            urlForCurrentChatAction = (user + ': ' if not user == '' else '') + googleBooksUrl
            bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)
    else:
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
                                  ', I\'m afraid I can\'t find any books for ' +\
                                  requestText.encode('utf-8') + '.'
        bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)
