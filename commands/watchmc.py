# coding=utf-8

from google.appengine.ext import ndb

import main
from commands.mc import get_mc_data

watchedCommandName = 'mc'


class WatchValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')


# ================================

def setWatchValue(chat_id, NewValue):
    es = WatchValue.get_or_insert(str(chat_id) + ':' + watchedCommandName)
    es.currentValue = NewValue.split(' players ')[0]
    es.put()


def getWatchValue(chat_id):
    es = WatchValue.get_by_id(str(chat_id) + ':' + watchedCommandName)
    if es:
        return es.currentValue
    return ''

def run(bot, keyConfig, chat_id, user, message='', intention_confidence=0.0):
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
                                text='Watch for /' + watchedCommandName + ' has not changed:\n' +
                                     getData)
        if not main.AllWatchesContains(watchedCommandName, chat_id):
            main.addToAllWatches(watchedCommandName, chat_id)
    else:
        bot.sendMessage(chat_id=chat_id, text=mc_server_not_found_message)


def unwatch(bot, chat_id, message):
    watches = main.getAllWatches()
    if ',' + str(chat_id) + ':' + watchedCommandName + ',' in watches \
            or ',' + str(chat_id) + ':' + watchedCommandName in watches:
        main.removeFromAllWatches(str(chat_id) + ':' + watchedCommandName)
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' has been removed.')
    else:
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' not found.')
    if getWatchValue(chat_id) != '':
        setWatchValue(chat_id, '')