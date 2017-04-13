# coding=utf-8

from google.appengine.ext import ndb
from commands.mc import get_mc_data

watchedCommandName = 'mc'


class MCWatchValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')
    all_chat_ids = ndb.StringProperty(indexed=False, default='')


# ================================

def setWatchValue(chat_id, NewValue):
    es = MCWatchValue.get_or_insert(str(chat_id) + ':' + watchedCommandName)
    es.currentValue = NewValue.split(' players ')[0]
    es.put()


def getWatchValue(chat_id):
    es = MCWatchValue.get_by_id(str(chat_id) + ':' + watchedCommandName)
    if es:
        return es.currentValue
    return ''

def addToAllWatches(chat_id):
    es = MCWatchValue.get_or_insert(watchedCommandName + ':' + 'AllWatchers')
    es.all_chat_ids += ',' + str(chat_id)
    es.put()

def AllWatchesContains(chat_id):
    es = MCWatchValue.get_by_id(watchedCommandName + ':' + 'AllWatchers')
    if es:
        return (',' + str(chat_id)) in str(es.all_chat_ids) or \
               (str(chat_id) + ',') in str(es.all_chat_ids)
    return False

def setAllWatchesValue(NewValue):
    es = MCWatchValue.get_or_insert(watchedCommandName + ':' + 'AllWatchers')
    es.all_chat_ids = NewValue
    es.put()

def getAllWatches():
    es = MCWatchValue.get_by_id(watchedCommandName + ':' + 'AllWatchers')
    if es:
        return es.all_chat_ids
    return ''

def removeFromAllWatches(watch):
    setAllWatchesValue(getAllWatches().replace(',' + watch + ',', ',')
                       .replace(',' + watch, '')
                       .replace(watch + ',', ''))


def run(bot, chat_id, user, keyConfig, message='', totalResults=1):
    getData, mc_server_found, mc_server_not_found_message = get_mc_data(keyConfig, user)
    if mc_server_found:
        OldValue = getWatchValue(chat_id)
        if OldValue != getData.split(' players ')[0]:
            setWatchValue(chat_id, getData)
            if OldValue == '':
                if user != 'Watcher':
                    bot.sendMessage(chat_id=chat_id, text='Now watching /' + watchedCommandName + '\n' + getData)
            else:
                bot.sendMessage(chat_id=chat_id,
                                text='Watch for /' + watchedCommandName + ' has changed.\n' + getData)
        else:
            if user != 'Watcher':
                bot.sendMessage(chat_id=chat_id,
                                text='Watch for /' + watchedCommandName + ' has not changed:\n' + getData)
        if not AllWatchesContains(chat_id):
            addToAllWatches(chat_id)
    else:
        bot.sendMessage(chat_id=chat_id, text=mc_server_not_found_message)


def unwatch(bot, chat_id, message):
    watches = getAllWatches()
    if ',' + str(chat_id) + ':' + watchedCommandName + ',' in watches \
            or ',' + str(chat_id) + ':' + watchedCommandName in watches:
        removeFromAllWatches(str(chat_id))
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' has been removed.')
    else:
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' not found.')
    if getWatchValue(chat_id) != '':
        setWatchValue(chat_id, '')