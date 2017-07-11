# coding=utf-8
import uuid

from google.appengine.ext import ndb
import telegram

class LoginCodeValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')

class LoggedinValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.BooleanProperty(indexed=False, default='')


# ================================

def Login(chat_id):
    es = LoggedinValue.get_or_insert('loggedin:' + str(chat_id))
    es.currentValue = True
    es.put()

def Logout(chat_id):
    es = LoggedinValue.get_or_insert('loggedin:' + str(chat_id))
    es.currentValue = False
    es.put()

def getLoggedinValue(chat_id):
    es = LoggedinValue.get_by_id('loggedin:' + str(chat_id))
    if es:
        return es.currentValue
    return False

def setPin(chat_id, NewValue):
    es = LoginCodeValue.get_or_insert('logincode:' + str(chat_id))
    es.currentValue = NewValue
    es.put()

def getPin(chat_id):
    es = LoginCodeValue.get_by_id('logincode:' + str(chat_id))
    if es:
        return es.currentValue.encode('utf-8')
    return ''

def run(bot, chat_id, user='Dave', keyConfig=None, message='', totalResults=1):
    if message == '':
        bot.sendMessage(chat_id=chat_id, text='Username: ' + str(chat_id))
    elif message == getPin(chat_id):
        Login(chat_id)
        bot.sendMessage(chat_id=chat_id, text='Username: ' + str(chat_id) + '\nThat password is correct, you may proceed.')
    #elif chat_id == keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID') or chat_id == keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_GROUP_CHAT_ID'):
    #    bot.sendMessage(chat_id=chat_id, text='Username: ' + str(chat_id) + '\nYou are an admin!')

def generate_new_pin(chat_id):
    pin = getPin(chat_id)
    if pin != '':
        return pin
    loginCodeValue = str(uuid.uuid4())[:4]
    setPin(chat_id, loginCodeValue)
    return loginCodeValue