# coding=utf-8
import hashlib
import string
import urllib

from google.appengine.ext import ndb

import main
from commands import get
from commands import retry_on_telegram_error


class WatchValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')

# ================================

def setWatchValue(chat_id, request, NewValue):
    es = WatchValue.get_or_insert(str(chat_id) + ':' + request)
    es.currentValue = NewValue
    es.put()

def getWatchValue(chat_id, request):
    es = WatchValue.get_by_id(str(chat_id) + ':' + request)
    if es:
        return es.currentValue
    return ''

def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    requestText = message.replace(bot.name, "").strip()
    data = get.Google_Image_Search(keyConfig, message)
    if 'items' in data and len(data['items']) >= 1:
        imagelink = data['items'][0]['link']
        fd = urllib.urlopen(imagelink)
        fileHash = md5(fd.read())
        OldValue = getWatchValue(chat_id, requestText)
        if OldValue != fileHash:
            if not main.AllWatchesContains(chat_id, requestText):
                main.addToAllWatches(chat_id, requestText)
            setWatchValue(chat_id, requestText, fileHash)
            retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink, 'Now watching /get ' + requestText + '.', user)
        else:
            retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink, 'Watch for /get ' + requestText + ' has not changed.', user)
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t watch ' +
                                              'because I did not find any results for /get ' +
                                              string.capwords(requestText.encode('utf-8')))


def md5(byteStream):
    hash_md5 = hashlib.md5()
    hash_md5.update(byteStream)
    return hash_md5.hexdigest()