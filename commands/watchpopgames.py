# coding=utf-8

from google.appengine.ext import ndb

import main
from commands.getpopgames import get_steamcharts_top_games

watchedCommandName = 'getpopgames'
removed_games_title = '*Removed Games:*'
added_games_title = '*New Games:*'


class WatchValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')


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


def get_add_removed_games(new_list, old_list):
    added_games = added_games_title
    for item in new_list.split('\n'):
        if item not in old_list:
            added_games += '\n' + item
    removed_games = removed_games_title
    for item in old_list.split('\n'):
        if item not in new_list:
            removed_games += '\n' + item
    return added_games, removed_games


def run(bot, keyConfig, chat_id, user, message='', intention_confidence=0.0):
    pop_games = get_steamcharts_top_games()
    if pop_games:
        OldValue = getWatchValue(chat_id)
        if OldValue != pop_games:
            setWatchValue(chat_id, pop_games)
            if OldValue == '':
                if user != 'Watcher':
                    bot.sendMessage(chat_id=chat_id,
                                    text='Now watching /' + watchedCommandName + ' ' + message + '\n' + pop_games,
                                    parse_mode='Markdown')
            else:
                games_added, games_removed = get_add_removed_games(pop_games, OldValue)
                bot.sendMessage(chat_id=chat_id,
                                text='Watch for /' + watchedCommandName + ' ' + message + ' has changed' +
                                     (' order.' + games_added if (games_added == added_games_title and games_removed == removed_games_title) else '.') +
                                     '\n' + pop_games +
                                     ('\n' + games_added if games_added != added_games_title else '') +
                                     ('\n' + games_removed if games_removed != removed_games_title else ''),
                                parse_mode='Markdown')
        else:
            if user != 'Watcher':
                bot.sendMessage(chat_id=chat_id,
                                text='Watch for /' + watchedCommandName + ' ' + message + ' has not changed:\n' + pop_games,
                                parse_mode='Markdown')
        if not main.AllWatchesContains(watchedCommandName, chat_id, message):
            main.addToAllWatches(watchedCommandName, chat_id, message)
    else:
        bot.sendMessage(chat_id=chat_id,
                        text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                             ', I\'m afraid I can\'t watch ' +
                             'because I did not find any results from /' + watchedCommandName,
                        parse_mode='Markdown')


def unwatch(bot, chat_id):
    watches = main.getAllWatches()
    if ',' + str(chat_id) + ':' + watchedCommandName + ',' in watches or ',' + str(chat_id) + ':' + watchedCommandName in watches:
        main.removeFromAllWatches(str(chat_id) + ':' + watchedCommandName)
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' has been removed.')
    else:
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' not found.')
    if getWatchValue(chat_id) != '':
        setWatchValue(chat_id, '')
