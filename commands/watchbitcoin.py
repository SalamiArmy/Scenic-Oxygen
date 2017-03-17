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
        float_ready_current_price = priceZA.replace(',', '')
        OldValue = getWatchValue(chat_id)
        if OldValue != '':
            split_OldValue = OldValue.split(':')
            old_price = split_OldValue[0] if len(split_OldValue) == 2 else OldValue
            float_ready_old_price = old_price.replace(',', '')
            old_request_text = split_OldValue[1] if len(split_OldValue) == 2 else ''
            if old_request_text != message:
                unwatch(bot, chat_id, old_request_text)
                OldValue = ''
        else:
            old_price = ''
            float_ready_old_price = 0.0
        setWatchValue(chat_id, message, priceZA)
        price_diff = float(float_ready_current_price) - float(float_ready_old_price)
        if OldValue == '' and message == '' and user != 'Watcher':
            bot.sendMessage(chat_id=chat_id,
                            text='Now watching /' + watchedCommandName + ' ' + message + '\n' +
                                 'The Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                 ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
        elif OldValue == '' and (message[:1] == '+' or message[:1] == '-') and user != 'Watcher':
            bot.sendMessage(chat_id=chat_id,
                            text='Now watching /' + watchedCommandName + ' changes by ' + message + '\n' +
                                 'The Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                 ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
        elif OldValue == '' and message[:1] != '+' and message[:1] != '-' and user != 'Watcher':
            bot.sendMessage(chat_id=chat_id,
                            text='Now watching /' + watchedCommandName + ' changes below threshhold of ' + message + '\n' +
                                 'The Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                 ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
        elif old_price != priceZA and message == '':
            if user != 'Watcher':
                if OldValue != '':
                    bot.sendMessage(chat_id=chat_id,
                                    text='Watch for /' + watchedCommandName + ' ' + message + ' has changed by ' + str(price_diff) + ' ZAR:\n' +
                                         'The Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                         ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
            else:
                bot.sendMessage(chat_id=chat_id,
                                text='Watched /' + watchedCommandName + ' ' + message + ' changed by ' + str(price_diff) + ' ZAR:\n' +
                                     'The New Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                     ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
        elif (float(float_ready_old_price)-float(float_ready_current_price) > float(message) and message[:1] == '+') or \
                (float(float_ready_old_price)-float(float_ready_current_price) < float(message) and message[:1] == '-'):
            if user != 'Watcher':
                if OldValue != '':
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
        elif float(float_ready_current_price) < float(message) and (message[:1] != '+' and message[:1] != '-'):
            if user != 'Watcher':
                if OldValue != '':
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
                if message == '':
                    bot.sendMessage(chat_id=chat_id,
                                    text='Watch for /' + watchedCommandName + ' has not changed.' +
                                         'The Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                         ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
                elif message[:1] == '+' or message[:1] == '-':
                    bot.sendMessage(chat_id=chat_id,
                                    text='Watch for /' + watchedCommandName + ' has not changed by ' + message + '\n' +
                                         'The Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                         ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
                elif message[:1] != '+' and message[:1] != '-':
                    bot.sendMessage(chat_id=chat_id,
                                    text='Watch for /' + watchedCommandName + ' has not dropped below ' + message +' ZAR:\n' +
                                         'The Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB +
                                         ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
        if not main.AllWatchesContains(watchedCommandName, chat_id, message):
            main.addToAllWatches(watchedCommandName, chat_id, message)
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t watch ' +
                                              'because I did not find any results from /bitcoin')

def unwatch(bot, chat_id, message, sendmessage=False):
    watches = main.getAllWatches()
    if ',' + watchedCommandName + ':' + str(chat_id) + ':' + message + ',' in watches or ',' + watchedCommandName + ':' + str(chat_id) + ':' + message in watches:
        main.removeFromAllWatches(watchedCommandName + ':' + str(chat_id) + ':' + message)
        if sendmessage:
            bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' has been removed.')
    else:
        if sendmessage:
            bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' not found.')
    if getWatchValue(chat_id) != '':
        setWatchValue(chat_id, message, '')