# coding=utf-8
import uuid

from google.appengine.ext import ndb

class LoginCodeValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')

class LoginCountValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')

class LoggedinValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')

# ================================

def Login(chat_id):
    es = LoggedinValue.get_or_insert('loggedin:' + str(chat_id))
    es.currentValue = 'True'
    es.put()

def Logout(chat_id):
    es = LoggedinValue.get_or_insert('loggedin:' + str(chat_id))
    es.currentValue = 'False'
    es.put()

def getLoggedinValue(chat_id):
    es = LoggedinValue.get_by_id('loggedin:' + str(chat_id))
    if es:
        return es.currentValue
    return 'False'

def setPin(chat_id, NewValue):
    es = LoginCodeValue.get_or_insert('logincode:' + str(chat_id))
    es.currentValue = NewValue
    es.put()

def getPin(chat_id):
    es = LoginCodeValue.get_by_id('logincode:' + str(chat_id))
    if es:
        return es.currentValue.encode('utf-8')
    return ''

def setCount(chat_id, NewValue):
    es = LoginCountValue.get_or_insert('logincount:' + str(chat_id))
    es.currentValue = NewValue
    es.put()

def getCount(chat_id):
    es = LoginCountValue.get_by_id('logincount:' + str(chat_id))
    if es:
        return es.currentValue.encode('utf-8')
    return ''

def run(bot, chat_id, user='Dave', keyConfig=None, message='', totalResults=1):
    count = getCount(chat_id)
    if count and int(count) > 3:
        return bot.sendMessage(chat_id=chat_id, text='You have been locked out due to too many incorrect login attempts.')
    pin = getPin(chat_id)
    if chat_id == keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID') or chat_id == keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_GROUP_CHAT_ID'):
        bot.sendMessage(chat_id=chat_id, text='Username: ' + str(chat_id) + '\nYou are an admin!')
    elif getLoggedinValue(chat_id) == 'True':
        bot.sendMessage(chat_id=chat_id, text='You have already logged in.')
    elif message == pin:
        Login(chat_id)
        bot.sendMessage(chat_id=chat_id, text='That password is correct, you may proceed.')
    else:
        bot.sendMessage(chat_id=chat_id, text='Login requires the use of a One Time Pin which you can get by visitting:\n ' +
                                              keyConfig.get('InternetShortcut', 'URL') + '/login?username=' + chat_id + '\n' +
                                              'You have ' + incrementCount(chat_id, count) + ' remaining attempts to log in.')


def incrementCount(chat_id, count):
    if count:
        count = str(int(count) + 1)
    else:
        count = '1'
    setCount(chat_id, count)
    return count


def generate_new_pin(chat_id):
    if getLoggedinValue(chat_id) == 'True':
        return 'You have already logged in.'
    pin = getPin(chat_id)
    if pin != '':
        return pin
    loginCodeValue = str(uuid.uuid4())[:4]
    setPin(chat_id, loginCodeValue)
    return loginCodeValue