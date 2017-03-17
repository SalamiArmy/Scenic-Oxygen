# coding=utf-8

from google.appengine.ext import ndb

import main
from commands.gettopgames import get_steam_top_games

watchedCommandName = 'gettopgames'


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


def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    top_games = get_steam_top_games()
    if top_games:
        OldValue = getWatchValue(chat_id, message)
        if OldValue != top_games:
            setWatchValue(chat_id, message, top_games)
            if user != 'Watcher':
                if OldValue == '':
                    bot.sendMessage(chat_id=chat_id, text='Now watching /' + watchedCommandName + ' ' + message + '\n' + top_games, parse_mode='Markdown')
                else:
                    bot.sendMessage(chat_id=chat_id,
                                    text='Now watching /' + watchedCommandName + ' ' + message + '\n' + top_games, parse_mode='Markdown')
            else:
                bot.sendMessage(chat_id=chat_id,
                                text='Watch for /' + watchedCommandName + ' ' + message + ' has changed.\n' + top_games, parse_mode='Markdown')
        else:
            if user != 'Watcher':
                bot.sendMessage(chat_id=chat_id,
                                text='Watch for /' + watchedCommandName + ' ' + message + ' has not changed:\n' + top_games, parse_mode='Markdown')
        if not main.AllWatchesContains(watchedCommandName, chat_id, message):
            main.addToAllWatches(watchedCommandName, chat_id, message)
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t watch ' +
                                              'because I did not find any results from /' + watchedCommandName, parse_mode='Markdown')


def unwatch(bot, chat_id, message):
    watches = main.getAllWatches()
    if ',' + watchedCommandName + ':' + str(chat_id) + ':' + message + ',' in watches or ',' + watchedCommandName + \
            ':' + str(chat_id) + ':' + message in watches:
        main.removeFromAllWatches(watchedCommandName + ':' + str(chat_id) + ':' + message)
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' has been removed.')
    else:
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' not found.')
    if getWatchValue(chat_id, message) != '':
        setWatchValue(chat_id, message, '')