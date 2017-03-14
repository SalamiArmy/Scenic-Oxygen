# coding=utf-8
import string

from google.appengine.ext import ndb

import main
from commands import bitcoin

watchedCommandName = 'bitcoin'


class WatchValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')


# ================================

def setWatchValue(chat_id, NewValue):
    es = WatchValue.get_or_insert('bitcoin:' + str(chat_id))
    es.currentValue = NewValue
    es.put()


def getWatchValue(chat_id):
    es = WatchValue.get_by_id('bitcoin:' + str(chat_id))
    if es:
        return es.currentValue
    return ''


def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    priceGB, priceUS, priceZA, updateTime = bitcoin.get_bitcoin_prices()
    if priceZA:
        OldValue = getWatchValue(chat_id)
        if OldValue != priceZA:
            setWatchValue(chat_id, priceZA)
            if user != 'Watcher':
                bot.sendMessage(chat_id=chat_id,
                                text='Now watching /' + watchedCommandName + '\n' +
                                     'The Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                     ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
            else:
                bot.sendMessage(chat_id=chat_id,
                                text='Watched /' + watchedCommandName + ' changed:\n' +
                                     'The New Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                     ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
        else:
            if user != 'Watcher':
                bot.sendMessage(chat_id=chat_id,
                                text='Watch for /' + watchedCommandName + ' has not changed:\n' +
                                     'The Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                     ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
        if not main.AllWatchesContains(watchedCommandName, chat_id):
            main.addToAllWatches(watchedCommandName, chat_id)
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t watch ' +
                                              'because I did not find any results from /bitcoin')

