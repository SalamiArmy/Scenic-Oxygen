# coding=utf-8
import string

import sys
from google.appengine.ext import ndb

class SetValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')

# ================================

def setSetValue(chat_id, NewValue):
    es = SetValue.get_or_insert(str(chat_id))
    if es.currentValue == '':
        es.currentValue = NewValue
    else:
        es.currentValue = es.currentValue + ',' + NewValue
    es.put()

def getSetValue(chat_id):
    es = SetValue.get_by_id(str(chat_id))
    if es:
        return es.currentValue
    return ''

def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    try:
        requestText = message.replace(bot.name, "").strip()
        OldValue = getSetValue(chat_id)
        if OldValue == '':
            OldValue = 'blank'
        setSetValue(chat_id, requestText)
        bot.sendMessage(chat_id=chat_id, text='Chat ' + str(chat_id) + ' was:\n' + OldValue + '\nnow:\n' + requestText)
    except:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t set ' +
                                              string.capwords(requestText.encode('utf-8')) + '. ' + sys.exc_info()[0])


