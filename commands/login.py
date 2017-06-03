# coding=utf-8
import uuid

from google.appengine.ext import ndb
import telegram

watchedCommandName = 'login'

class LoginCodeValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')


# ================================

def setLoginCodeValue(chat_id, NewValue):
    es = LoginCodeValue.get_or_insert(watchedCommandName + ':' + str(chat_id))
    es.currentValue = NewValue
    es.put()

def getLoginCodeValue(chat_id):
    es = LoginCodeValue.get_by_id(watchedCommandName + ':' + str(chat_id))
    if es:
        return es.currentValue.encode('utf-8')
    return ''

def run(bot, chat_id, user='Dave', keyConfig=None, message='', totalResults=1):
    loginCodeValue = str(uuid.uuid4())[:4]
    setLoginCodeValue(chat_id, loginCodeValue)
    bot.sendMessage(chat_id=chat_id, text='Username: ' + str(chat_id) + '\nPassword: ' + loginCodeValue)