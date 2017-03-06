# coding=utf-8
import hashlib
import string

import sys
import urllib

import io
from google.appengine.ext import ndb

from commands import get


class WatchValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')

# ================================

def setWatchValue(chat_id, NewValue):
    es = WatchValue.get_or_insert(str(chat_id))
    es.currentValue = NewValue
    es.put()

def getWatchValue(chat_id):
    es = WatchValue.get_by_id(str(chat_id))
    if es:
        return es.currentValue
    return ''

def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    requestText = message.replace(bot.name, "").strip()
    data = get.Google_Image_Search(keyConfig, message)
    if 'items' in data and len(data['items']) >= 1:
        imagelink = data['items'][0]['link']
        fd = urllib.urlopen(imagelink)
        print("reading file...")
        fileHash = md5(fd.read())
        print("read hash as " + fileHash)
        OldValue = getWatchValue(chat_id)
        if OldValue == '':
            OldValue = 'blank'
        if OldValue != fileHash:
            setWatchValue(fileHash, requestText)
            bot.sendMessage(chat_id=chat_id, text='Chat ' + str(chat_id) + ' was:\n' + OldValue + '\nnow:\n' + fileHash)
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t watch ' +
                                              string.capwords(requestText.encode('utf-8')) + '. ')


def md5(byteStream):
    hash_md5 = hashlib.md5()
    hash_md5.update(byteStream)
    return hash_md5.hexdigest()