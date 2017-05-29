# coding=utf-8
import string

import main
from commands import getgif
from commands import get
from commands import retry_on_telegram_error

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    args = {'cx': keyConfig.get('Google', 'GCSE_GIF_SE_ID1'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': "image",
            'safe': "off",
            'q': requestText,
            'fileType': 'gif',
            'start': 1}
    data, total_results, results_this_page = get.Google_Custom_Search(args)
    if 'items' in data and results_this_page >= 0:
        offset_this_page = 0
        while offset_this_page < results_this_page:
            imagelink = data['items'][offset_this_page]['link']
            offset_this_page += 1
            if '?' in imagelink:
                imagelink = imagelink[:imagelink.index('?')]
            if getgif.is_valid_gif(imagelink):
                if not getgif.wasPreviouslySeenGif(chat_id, imagelink):
                    getgif.addPreviouslySeenGifsValue(chat_id, imagelink)
                    if user != 'Watcher':
                        bot.sendMessage(chat_id=chat_id, text='Now watching /' +
                                                              getgif.CommandName + ' ' + requestText + '.')
                        retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, user)
                    else:
                        bot.sendMessage(chat_id=chat_id, text='Watched /' +
                                                              getgif.CommandName + ' ' + requestText + ' changed.')
                        retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, user)
                else:
                    if user != 'Watcher':
                        bot.sendMessage(chat_id=chat_id, text=user + ', watch for /' +
                                                              getgif.CommandName + ' ' + requestText + ' has not changed.')
                        retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, user)
                break
        if not main.AllWatchesContains(getgif.CommandName, chat_id, requestText):
            main.addToAllWatches(getgif.CommandName, chat_id, requestText)
    else:
        if user != 'Watcher':
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t watch ' +
                                                  'because I did not find any results for /getgif ' +
                                                  string.capwords(requestText.encode('utf-8')))


def unwatch(bot, chat_id, message):
    watches = main.getAllWatches()
    if ',' + str(chat_id) + ':' + getgif.CommandName + ':' + message + ',' in watches or \
            watches.startswith(str(chat_id) + ':' + getgif.CommandName + ':' + message + ',') or \
            watches.endswith(',' + str(chat_id) + ':' + getgif.CommandName + ':' + message) or \
                    watches == str(chat_id) + ':' + getgif.CommandName + ':' + message:
        main.removeFromAllWatches(str(chat_id) + ':' + getgif.CommandName + ':' + message)
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + getgif.CommandName + ' ' + message + ' has been removed.')
    else:
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + getgif.CommandName + ' ' + message + ' not found.')
