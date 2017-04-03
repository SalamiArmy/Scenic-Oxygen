# coding=utf-8
import hashlib
import string
import urllib

from google.appengine.ext import ndb

import main
from commands import get
from commands import retry_on_telegram_error

watchedCommandName = 'get'


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
    data = get.Google_Image_Search(keyConfig, message)
    if 'items' in data and len(data['items']) >= 9:
        OldValue = getWatchValue(chat_id, requestText)
        imagelinks = data['items'][0]['link']
        count = 0
        for link in data['items']:
            imagelinks += '\n' + link['link']
        print('got image links for ' + requestText + ' as ' + imagelinks)
        for link in data['items']:
            imagelink = link['link']
            count += 1
            if OldValue != imagelinks:
                if user != 'Watcher':
                    retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink,
                                                               'Now watching /' + watchedCommandName + ' ' + requestText + '.' +
                                                               '\nThis is number ' + str(count) + '.'
                                                               ' number ' + str(count) + '.',
                                                               user)
                else:
                    retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink,
                                                               'Watched /' + watchedCommandName + ' ' + requestText +
                                                               ' changed.' +
                                                               '\nThis is number ' + str(count) + '.', user)
            else:
                if user != 'Watcher':
                    retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink,
                                                               'Watch for /' + watchedCommandName + ' ' + requestText +
                                                               ' has not changed.' +
                                                               '\nThis is number ' + str(count) + '.', user)
        print('Comparing ' + OldValue + ' with ' + imagelinks)
        if OldValue != imagelinks:
            setWatchValue(chat_id, requestText, imagelinks)
        if not main.AllWatchesContains(watchedCommandName, chat_id, requestText):
            main.addToAllWatches(watchedCommandName, chat_id, requestText)
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t watch ' +
                                              'because I did not find any results for /get ' +
                                              string.capwords(requestText.encode('utf-8')))

def md5(byteStream):
    hash_md5 = hashlib.md5()
    hash_md5.update(byteStream)
    return hash_md5.hexdigest()


def unwatch(bot, chat_id, message):
    watches = main.getAllWatches()
    if ',' + str(chat_id) + ':' + watchedCommandName + ':' + message + ',' in watches or \
                                                            ',' + str(chat_id) + ':' + watchedCommandName + ':' + message in watches:
        main.removeFromAllWatches(str(chat_id) + ':' + watchedCommandName + ':' + message)
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' has been removed.')
    else:
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' not found.')
    if getWatchValue(chat_id, message) != '':
        setWatchValue(chat_id, message, '')