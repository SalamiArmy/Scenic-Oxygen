# coding=utf-8
import string

from google.appengine.ext import ndb

import main
from commands import getgif
from commands import retry_on_telegram_error

watchedCommandName = 'getgif'


class WatchValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')


# ================================

def setWatchValue(chat_id, request, NewValue):
    es = WatchValue.get_or_insert(watchedCommandName + ':' + str(chat_id) + ':' + request)
    es.currentValue = NewValue
    es.put()


def getWatchValue(chat_id, request):
    es = WatchValue.get_by_id(watchedCommandName + ':' + str(chat_id) + ':' + request)
    if es:
        return es.currentValue
    return ''


def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    requestText = message.replace(bot.name, "").strip()
    data = getgif.search_google_for_gifs(keyConfig, requestText)
    if 'items' in data and len(data['items']) >= 1:
        offset = -1
        thereWasAnError = True
        while thereWasAnError and offset < len(data['items'])-1:
            offset += 1
            imagelink = data['items'][offset]['link']
            thereWasAnError = not getgif.isGifAnimated(imagelink)
        if not thereWasAnError:
            print('got image link for ' + requestText + ' as ' + imagelink)
            print('requesting the value for getgif:' + str(chat_id) + ':' + requestText)
            OldValue = getWatchValue(chat_id, requestText)
            print('Got watch value as ' + OldValue)
            print('Comparing ' + OldValue + ' with ' + imagelink)
            if OldValue != imagelink:
                if user != 'Watcher':
                    bot.sendMessage(chat_id=chat_id, text='Now watching /' +
                                                          watchedCommandName + ' ' + requestText + '.')
                    retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, user)
                else:
                    bot.sendMessage(chat_id=chat_id, text='Watched /' +
                                                          watchedCommandName + ' ' + requestText + ' changed.')
                    retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, user)
                if not thereWasAnError:
                    print('Setting watch value to ' + imagelink)
                    setWatchValue(chat_id, requestText, imagelink)
            else:
                if user != 'Watcher':
                    bot.sendMessage(chat_id=chat_id, text=user + ', watch for /' +
                                                          watchedCommandName + ' ' + requestText + ' has not changed.')
                    retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, user)
            if not main.AllWatchesContains(watchedCommandName, chat_id, requestText):
                main.addToAllWatches(watchedCommandName, chat_id, requestText)
        else:
            if user != 'Watcher':
                bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      ', I\'m afraid I can\'t watch ' +
                                                      'because I did not find any results for /getgif ' +
                                                      string.capwords(requestText.encode('utf-8')))
    else:
        if user != 'Watcher':
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t watch ' +
                                                  'because I did not find any results for /getgif ' +
                                                  string.capwords(requestText.encode('utf-8')))


def unwatch(bot, chat_id, message):
    watches = main.getAllWatches()
    if ',' + str(chat_id) + ':' + watchedCommandName + ':' + message + ',' in watches or ',' + str(chat_id) + ':' + watchedCommandName + ':' + message in watches:
        main.removeFromAllWatches(str(chat_id) + ':' + watchedCommandName + ':' + message)
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' has been removed.')
    else:
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' not found.')
    if getWatchValue(chat_id, message) != '':
        setWatchValue(chat_id, message, '')