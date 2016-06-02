# coding=utf-8
import json
import urllib

import telegram

from commands import retry_on_telegram_error


def run(bot, keyConfig, chat_id, user, message):
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
            retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, bookData['imageLinks']['thumbnail'], requestText, user)
        else:
            bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') + googleBooksUrl)
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +\
                                              ', I\'m afraid I can\'t find any books for ' +\
                                              requestText.encode('utf-8') + '.')
