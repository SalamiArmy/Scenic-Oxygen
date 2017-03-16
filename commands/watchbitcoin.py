# coding=utf-8
import string

from google.appengine.ext import ndb

import main
from commands import bitcoin
from commands import unwatchbitcoin

watchedCommandName = 'bitcoin'


class WatchValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')


# ================================

def setWatchValue(chat_id, request_text, NewValue):
    es = WatchValue.get_or_insert(watchedCommandName + ':' + str(chat_id))
    es.currentValue = NewValue + (':' + request_text if request_text != '' else '')
    es.put()


def getWatchValue(chat_id):
    es = WatchValue.get_by_id(watchedCommandName + ':' + str(chat_id))
    if es:
        return es.currentValue
    return ''


def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    priceGB, priceUS, priceZA, updateTime = bitcoin.get_bitcoin_prices()
    if priceZA:
        OldValue = getWatchValue(chat_id)
        old_price = OldValue.split(':')[0]
        old_request_text = OldValue.split(':')[1]
        float_ready_old_price = old_price.replace(',', '')
        float_ready_current_price = priceZA.replace(',', '')
        price_diff = float(float_ready_current_price) - float(float_ready_old_price)
        if OldValue != '' and old_request_text != message:
            unwatchbitcoin.run(bot, keyConfig, chat_id, user, old_request_text)
        if old_price != priceZA and message == '':
            setWatchValue(chat_id, message, priceZA)
            if user != 'Watcher':
                if OldValue == '':
                    bot.sendMessage(chat_id=chat_id,
                                    text='Now watching /' + watchedCommandName + ' ' + message + '\n' +
                                         'The Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                         ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
                else:
                    bot.sendMessage(chat_id=chat_id,
                                    text='Watch for /' + watchedCommandName + ' ' + message + ' has changed by ' + str(price_diff) + ' ZAR:\n' +
                                         'The Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                         ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
            else:
                bot.sendMessage(chat_id=chat_id,
                                text='Watched /' + watchedCommandName + ' ' + message + ' changed by ' + str(price_diff) + ' ZAR:\n' +
                                     'The New Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                     ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
        elif float(float_ready_old_price)-float(float_ready_current_price)>float(message) and (message[:1]=='+' or message[:1]=='-'):
            setWatchValue(chat_id, message, priceZA)
            if user != 'Watcher':
                if OldValue == '':
                    bot.sendMessage(chat_id=chat_id,
                                    text='Now watching /' + watchedCommandName + ' changes by ' + message + '\n' +
                                         'The Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                         ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
                else:
                    bot.sendMessage(chat_id=chat_id,
                                    text='Watch for /' + watchedCommandName + ' has changed by ' + str(price_diff) +
                                         ' ZAR. Which is greater than the tolerance of ' + message +':\n' +
                                         'The Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                         ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
            else:
                bot.sendMessage(chat_id=chat_id,
                                text='Watched /' + watchedCommandName + ' changed by ' + str(price_diff) +
                                     ' ZAR. Which is greater than the tolerance of ' + message +':\n' +
                                     'The New Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                     ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
        elif float(float_ready_current_price)<float(message) and (message[:1]!='+' and message[:1]!='-'):
            setWatchValue(chat_id, message, priceZA)
            if user != 'Watcher':
                if OldValue == '':
                    bot.sendMessage(chat_id=chat_id,
                                    text='Now watching /' + watchedCommandName + ' changes below threshhold of ' + message + '\n' +
                                         'The Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                         ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
                else:
                    bot.sendMessage(chat_id=chat_id,
                                    text='Watch for /' + watchedCommandName + ' has dropped below ' + message +' ZAR:\n' +
                                         'The Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                         ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
            else:
                bot.sendMessage(chat_id=chat_id,
                                text='Watched /' + watchedCommandName + ' has dropped below ' + message +' ZAR:\n' +
                                     'The New Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                     ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
        else:
            if user != 'Watcher':
                bot.sendMessage(chat_id=chat_id,
                                text='Watch for /' + watchedCommandName + ' has dropped below ' + message +' ZAR:\n' +
                                     'The Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                     ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
        if not main.AllWatchesContains(watchedCommandName, chat_id, message):
            main.addToAllWatches(watchedCommandName, chat_id, message)
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t watch ' +
                                              'because I did not find any results from /bitcoin')

