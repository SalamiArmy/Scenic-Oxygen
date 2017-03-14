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
    es = WatchValue.get_or_insert('get:' + str(chat_id) + ':' + request)
    es.currentValue = NewValue
    es.put()


def getWatchValue(chat_id, request):
    es = WatchValue.get_by_id('get:' + str(chat_id) + ':' + request)
    if es:
        return es.currentValue
    return ''


def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    requestText = message.replace(bot.name, "").strip()
    data = get.Google_Image_Search(keyConfig, message)
    if 'items' in data and len(data['items']) >= 1:
        imagelink = data['items'][0]['link']
        print('got image link for ' + requestText + ' as ' + imagelink)
        fd = urllib.urlopen(imagelink)
        fileHash = md5(fd.read())
        print('requesting the value for ' + str(chat_id) + ':' + requestText)
        OldValue = getWatchValue(chat_id, requestText)
        print('Comparing ' + OldValue + ' with ' + fileHash)
        if OldValue != fileHash:
            setWatchValue(chat_id, requestText, fileHash)
            if user != 'Watcher':
                retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink,
                                                           'Now watching /' + watchedCommandName + ' ' + requestText + '.',
                                                           user)
            else:
                retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink,
                                                           'Watched /' + watchedCommandName + ' ' + requestText +
                                                           ' changed.', user)
        else:
            if user != 'Watcher':
                retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink,
                                                           'Watch for /' + watchedCommandName + ' ' + requestText +
                                                           ' has not changed.', user)
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
