# coding=utf-8
import uuid

from google.appengine.ext import ndb

class LoginCodeValue(ndb.Model):
    # key name: chat_id
    currentValue = ndb.StringProperty(indexed=False, default='')

class LoginCountValue(ndb.Model):
    # key name: chat_id
    currentValue = ndb.IntegerProperty(indexed=False, default=0)

# ================================

def setPin(chat_id, NewValue):
    es = LoginCodeValue.get_or_insert(chat_id)
    es.currentValue = NewValue
    es.put()

def getPin(chat_id):
    es = LoginCodeValue.get_by_id(chat_id)
    if es:
        return str(es.currentValue)
    return ''

def setCount(chat_id, NewValue):
    es = LoginCountValue.get_or_insert(chat_id)
    es.currentValue = int(NewValue)
    es.put()

def getCount(chat_id):
    es = LoginCountValue.get_by_id(chat_id)
    if es:
        return int(es.currentValue)
    return 0

def incrementCount(chat_id, count):
    count = count + 1
    setCount(chat_id, count)
    return count

def generate_new_pin(chat_id):
    loginCodeValue = str(uuid.uuid4())[:4]
    setPin(chat_id, loginCodeValue)
    return loginCodeValue

def run(bot, chat_id, user='Dave', keyConfig=None, message='', totalResults=1):
    str_chat_id = str(chat_id)
    pin = generate_new_pin(str_chat_id)
    bot.sendMessage(chat_id=chat_id, text=user + ', your new One Time Pin for ' + str_chat_id +
                                          ' is hidden from preview below:\n\n\n\n\n\n\n\n' + pin)
    return 'New One Time Pin sent to ' + str_chat_id
