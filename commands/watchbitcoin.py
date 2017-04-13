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


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    priceGB, priceUS, new_price, updateTime = bitcoin.get_bitcoin_prices()
    if new_price:
        OldValue = getWatchValue(chat_id)
        float_ready_new_price = new_price.replace(',', '')
        new_price_float = float(float_ready_new_price)
        OldValue, old_price_float = parse_old_price_float(OldValue, bot, chat_id, message)
        price_diff = new_price_float - old_price_float
        setWatchValue(chat_id, message, new_price)
        formatted_price = 'The Current Price of 1 Bitcoin:\n\n' + priceUS + ' USD\n' + priceGB + ' GBP\n' + new_price + ' ZAR' + '\n\nTime Updated: ' + updateTime
        if OldValue == '' and message == '' and user != 'Watcher':
            bot.sendMessage(chat_id=chat_id,
                            text='Now watching /' + watchedCommandName + ' ' + message + '\n' + formatted_price)
        elif OldValue == '' and (message[:1] == '+' or message[:1] == '-') and user != 'Watcher':
            bot.sendMessage(chat_id=chat_id,
                            text='Now watching /' + watchedCommandName + ' changes by ' + message + '\n' + formatted_price)
        elif OldValue == '' and message[:1] != '+' and message[:1] != '-' and user != 'Watcher':
            bot.sendMessage(chat_id=chat_id,
                            text='Now watching /' + watchedCommandName + ' drops below threshold of ' + message + '\n' + formatted_price)
        elif old_price_float != new_price_float and message == '' and user != 'Watcher':
            if OldValue != '':
                bot.sendMessage(chat_id=chat_id,
                                text='Watch for /' + watchedCommandName + ' ' + message + ' has changed by ' + str(price_diff) + ' ZAR:\n' + formatted_price)
        elif old_price_float != new_price_float and message == '':
                bot.sendMessage(chat_id=chat_id,
                                text='Watched /' + watchedCommandName + ' ' + message + ' changed by ' + str(price_diff) + ' ZAR:\n' + formatted_price)
        elif price_diff > float(message) and message[:1] == '+':
            bot.sendMessage(chat_id=chat_id,
                            text='Watch for /' + watchedCommandName + ' has jumped by ' + str(price_diff) +
                                 ' ZAR. Which is higher than the tolerance of ' + message +':\n' + formatted_price)
        elif price_diff < float(message) and message[:1] == '-':
            bot.sendMessage(chat_id=chat_id,
                            text='Watch for /' + watchedCommandName + ' has dropped by ' + str(price_diff) +
                                 ' ZAR. Which is lower than the tolerance of ' + message +':\n' + formatted_price)
        elif new_price_float < float(message) and (message[:1] != '+' and message[:1] != '-'):
            bot.sendMessage(chat_id=chat_id,
                            text='Watch for /' + watchedCommandName + ' has dropped below ' + message +' ZAR:\n' + formatted_price)
        else:
            if user != 'Watcher':
                if message == '':
                    bot.sendMessage(chat_id=chat_id,
                                    text='Watch for /' + watchedCommandName + ' has not changed.\n' + formatted_price)
                elif message[:1] == '+' or message[:1] == '-':
                    bot.sendMessage(chat_id=chat_id,
                                    text='Watch for /' + watchedCommandName + ' has changed by ' + str(price_diff) +
                                         ' ZAR. Which is not ' + ('higher' if message[:1] == '+' else 'lower') + ' than the tolerance of ' + message +':\n' + formatted_price)
                elif message[:1] != '+' and message[:1] != '-':
                    bot.sendMessage(chat_id=chat_id,
                                    text='Watch for /' + watchedCommandName + ' has not dropped below ' + message +' ZAR:\n' + formatted_price)
        if not main.AllWatchesContains(watchedCommandName, chat_id, message):
            main.addToAllWatches(watchedCommandName, chat_id, message)
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t watch ' +
                                              'because I did not find any results from /bitcoin')


def parse_old_price_float(OldValue, bot, chat_id, message):
    if OldValue != '':
        split_OldValue = OldValue.split(':')
        old_price = split_OldValue[0] if len(split_OldValue) == 2 else OldValue
        float_ready_old_price = old_price.replace(',', '')
        old_request_text = split_OldValue[1] if len(split_OldValue) == 2 else ''
        if old_request_text != message:
            unwatch(bot, chat_id, old_request_text)
            OldValue = ''
    else:
        float_ready_old_price = '0.0'
    old_price_float = float(float_ready_old_price)
    return OldValue, old_price_float


def unwatch(bot, chat_id, message, sendmessage=False):
    watches = main.getAllWatches()
    if ',' + str(chat_id) + ':' + watchedCommandName + ':' + message + ',' in watches or ',' + str(chat_id) + ':' + watchedCommandName + ':' + message in watches:
        main.removeFromAllWatches(str(chat_id) + ':' + watchedCommandName + ':' + message)
        if sendmessage:
            bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' has been removed.')
    else:
        if sendmessage:
            bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' not found.')
    if getWatchValue(chat_id) != '':
        setWatchValue(chat_id, '', '')
