# coding=utf-8

from google.appengine.ext import ndb
from commands import cric

watchedCommandName = 'cric'


class WatchValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')
    all_chat_ids = ndb.StringProperty(indexed=False, default='')


# ================================

def setWatchValue(chat_id, NewValue):
    es = WatchValue.get_or_insert(watchedCommandName + ':' + str(chat_id))
    es.currentValue = NewValue
    es.put()


def getWatchValue(chat_id):
    es = WatchValue.get_by_id(watchedCommandName + ':' + str(chat_id))
    if es:
        return es.currentValue
    return ''

def addToAllWatches(chat_id):
    es = WatchValue.get_or_insert(watchedCommandName + ':' + 'AllWatchers')
    es.all_chat_ids += ',' + str(chat_id)
    es.put()

def AllWatchesContains(chat_id):
    es = WatchValue.get_by_id(watchedCommandName + ':' + 'AllWatchers')
    if es:
        return (',' + str(chat_id)) in str(es.all_chat_ids) or \
               (str(chat_id) + ',') in str(es.all_chat_ids)
    return False

def setAllWatchesValue(NewValue):
    es = WatchValue.get_or_insert(watchedCommandName + ':' + 'AllWatchers')
    es.all_chat_ids = NewValue
    es.put()

def getAllWatches():
    es = WatchValue.get_by_id(watchedCommandName + ':' + 'AllWatchers')
    if es:
        return es.all_chat_ids
    return ''

def removeFromAllWatches(watch):
    setAllWatchesValue(getAllWatches().replace(',' + watch + ',', ',')
                       .replace(',' + watch, '')
                       .replace(watch + ',', ''))


def run(bot, chat_id, user, keyConfig, message='', totalResults=1):
    getData = cric.get_cric_data(user)
    if getData:
        OldValue = getWatchValue(chat_id)
        if OldValue != getData:
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
                                text='Watch for /' + watchedCommandName + ' has not changed:\n' +
                                     getData)
        if not AllWatchesContains(watchedCommandName, chat_id):
            addToAllWatches(watchedCommandName, chat_id)
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t watch ' +
                                              'because I did not find any results from /' + watchedCommandName)


def unwatch(bot, chat_id):
    watches = getAllWatches()
    if ',' + str(chat_id) + ':' + watchedCommandName + ',' in watches \
            or ',' + str(chat_id) + ':' + watchedCommandName in watches:
        removeFromAllWatches(str(chat_id) + ':' + watchedCommandName)
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' has been removed.')
    else:
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' not found.')
    if getWatchValue(chat_id) != '':
        setWatchValue(chat_id, '')
