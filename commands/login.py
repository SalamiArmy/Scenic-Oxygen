# coding=utf-8
import uuid

from google.appengine.ext import ndb

class LoginCodeValue(ndb.Model):
    # key name: chat_id
    currentValue = ndb.StringProperty(indexed=False, default='')

class LoginCountValue(ndb.Model):
    # key name: chat_id
    currentValue = ndb.IntegerProperty(indexed=False, default=0)

class LoggedinValue(ndb.Model):
    # key name: chat_id
    currentValue = ndb.StringProperty(indexed=False, default='')

# ================================

def Login(chat_id):
    es = LoggedinValue.get_or_insert('loggedin:' + chat_id)
    es.currentValue = 'True'
    es.put()

def Logout(chat_id):
    es = LoggedinValue.get_or_insert('loggedin:' + chat_id)
    es.currentValue = 'False'
    es.put()

def getLoggedinValue(chat_id):
    es = LoggedinValue.get_by_id('loggedin:' + chat_id)
    if es:
        return es.currentValue
    return 'False'

def setPin(chat_id, NewValue):
    es = LoginCodeValue.get_or_insert('logincode:' + chat_id)
    es.currentValue = NewValue
    es.put()

def getPin(chat_id):
    es = LoginCodeValue.get_by_id('logincode:' + chat_id)
    if es:
        return str(es.currentValue)
    return ''

def setCount(chat_id, NewValue):
    es = LoginCountValue.get_or_insert('logincount:' + chat_id)
    es.currentValue = int(NewValue)
    es.put()

def getCount(chat_id):
    es = LoginCountValue.get_by_id('logincount:' + chat_id)
    if es:
        return int(es.currentValue)
    return 0

def run(bot, chat_id, user='Dave', keyConfig=None, message='', totalResults=1):
    str_chat_id = str(chat_id)
    count = getCount(str_chat_id)
    if count > 3:
        return bot.sendMessage(chat_id=str_chat_id, text='You have been locked out due to too many incorrect login attempts.')
    pin = getPin(str_chat_id)
    if str_chat_id == keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID') or str_chat_id == keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_GROUP_CHAT_ID'):
        bot.sendMessage(chat_id=str_chat_id, text='Username: ' + str_chat_id + '\nYou are an admin!')
    elif getLoggedinValue(str_chat_id) == 'True':
        bot.sendMessage(chat_id=str_chat_id, text='You have already logged in.')
    elif message == pin:
        Login(str_chat_id)
        bot.sendMessage(chat_id=str_chat_id, text='That password is correct, you may proceed.')
    else:
        bot.sendMessage(chat_id=str_chat_id, text='Login requires the use of a One Time Pin which you can get by visitting:\n ' +
                                              keyConfig.get('InternetShortcut', 'URL') + '/login?username=' + str_chat_id + '\n' +
                                              'You have ' + str(incrementCount(str_chat_id, count)) + ' remaining attempts to log in.')


def incrementCount(chat_id, count):
    if count:
        count = int(count) + 1
    else:
        count = 1
    setCount(chat_id, count)
    return int(count)


def generate_new_pin(chat_id):
    if getLoggedinValue(chat_id) == 'True':
        return 'You have already logged in.'
    pin = getPin(chat_id)
    if pin != '':
        return pin
    loginCodeValue = str(uuid.uuid4())[:4]
    setPin(chat_id, loginCodeValue)
    return loginCodeValue