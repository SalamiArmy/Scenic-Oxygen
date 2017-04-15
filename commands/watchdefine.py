# coding=utf-8
from google.appengine.ext import ndb

import main
from commands import define

watchedCommandName = 'define'


class WatchValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')


# ================================

def setWatchValue(chat_id, request, NewValue):
    es = WatchValue.get_or_insert(watchedCommandName + ':' + str(chat_id) + ':' + request)
    es.currentValue = NewValue
    es.put()


def getWatchValue(chat_id, request):
    es = WatchValue.get_by_id(watchedCommandName + ':' + str(chat_id) + ':' + request)
    if es:
        return es.currentValue
    return ''


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    getData = define.get_define_data(keyConfig, user, message)
    if ('<blockquote>' not in getData):
        OldValue = getWatchValue(chat_id, message)
        if OldValue != getData:
            setWatchValue(chat_id, message, getData)
            if OldValue == '':
                if user != 'Watcher':
                    bot.sendMessage(chat_id=chat_id,
                                        text='Now watching /' + watchedCommandName + ' ' + message + '\n' + getData)
            else:
                bot.sendMessage(chat_id=chat_id,
                                text='Watch for /' + watchedCommandName + ' ' + message + ' has changed.\n' + getData)
        else:
            if user != 'Watcher':
                bot.sendMessage(chat_id=chat_id,
                                text='Watch for /' + watchedCommandName + ' ' + message + ' has not changed:\n' + getData)
        if not main.AllWatchesContains(watchedCommandName, chat_id, message):
            main.addToAllWatches(watchedCommandName, chat_id, message)
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t watch ' +
                                              'because I did not find any results from /' + watchedCommandName)


def unwatch(bot, chat_id, message):
    watches = main.getAllWatches()
    if ',' + str(chat_id) + ':' + watchedCommandName + ':' + message + ',' in watches or ',' + str(chat_id) + \
            ':' + watchedCommandName + ':' + message in watches:
        main.removeFromAllWatches(str(chat_id) + ':' + watchedCommandName + ':' + message)
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' has been removed.')
    else:
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' not found.')
    if getWatchValue(chat_id, message) != '':
        setWatchValue(chat_id, message, '')