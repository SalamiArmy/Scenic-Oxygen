# coding=utf-8
import json
import urllib

import telegram

from commands import retry_on_telegram_error
from commands import get


def run(bot, chat_id, user, keyConfig, message):
    requestText = message.replace(bot.name, "").strip()
    data, total_results, results_this_page = search_google_for_figs(keyConfig, requestText)
    if 'items' in data and total_results > 0:
        total_offset = 0
        thereWasAnError = True
        while thereWasAnError and total_offset < total_results:
            offset_this_page = 0
            thereWasAnError = True
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            while thereWasAnError and offset_this_page < results_this_page:
                imagelink = data['items'][offset_this_page]['link']
                offset_this_page += 1
                total_offset += 1
                if '?' in imagelink:
                    imagelink = imagelink[:imagelink.index('?')]
                if not imagelink.startswith('x-raw-image:///') and imagelink != '' and not get.wasPreviouslySeenImage(chat_id, imagelink):
                    thereWasAnError = not retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink, requestText)
                get.addPreviouslySeenImagesValue(chat_id, imagelink)
            if thereWasAnError:
                data, total_results, results_this_page = search_google_for_figs(keyConfig, requestText, total_offset+1)
        if (thereWasAnError or not total_offset < total_results):
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find any figs.')
        else:
            return True
    else:
        if 'error' in data:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  data['error']['message'])
        else:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find any figs.')

def search_google_for_figs(keyConfig, requestText, startIndex=1):
    googurl = 'https://www.googleapis.com/customsearch/v1'
    args = {'cx': keyConfig.get('Google', 'GCSE_SE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': 'image',
            'safe': 'off',
            'q': 'fig',
            'start': startIndex}
    realUrl = googurl + '?' + urllib.urlencode(args)
    data = json.load(urllib.urlopen(realUrl))
    total_results = 0
    results_this_page = 0
    if 'searchInformation' in data and 'totalResults' in data['searchInformation']:
        total_results = data['searchInformation']['totalResults']
    if 'queries' in data and 'request' in data['queries'] and len(data['queries']['request']) > 0 and 'count' in \
            data['queries']['request'][0]:
        results_this_page = data['queries']['request'][0]['count']
    return data, total_results, results_this_page