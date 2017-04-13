# coding=utf-8
import string
import uuid

import telegram
from google.appengine.ext import ndb

import main
from commands import iss

watchedCommandName = 'iss'


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
    requestText = message.replace(bot.name, "").strip()

    has_iss_results, has_place_results, startDateTime, durationSeconds = iss.get_iss_data(keyConfig, requestText)
    if has_place_results:
        if has_iss_results:
            if has_iss_results:
                OldValue = getWatchValue(chat_id)
                if OldValue != startDateTime:
                    setWatchValue(chat_id, requestText, startDateTime)
                if OldValue == '' and user != 'Watcher' and message == '':
                    url = 'http://www.heavens-above.com/orbitdisplay.aspx?icon=iss&width=400&height=400&satid=25544&uuid=' + \
                          str(uuid.uuid4())
                    bot.sendMessage(chat_id=chat_id,
                                    text='Now watching /' + watchedCommandName + ' ' + message + '\n' +
                                         iss.format_iss_message(durationSeconds, requestText, startDateTime) + '\n' +
                                         url)
                elif OldValue == '' and user != 'Watcher' and message != '':
                    bot.sendMessage(chat_id=chat_id,
                                    text='Now watching /' + watchedCommandName + ' changes by ' + message + '\n' +
                                         iss.format_iss_message(durationSeconds, requestText, startDateTime))
                elif OldValue != '' and user != 'Watcher' and message == '':
                    url = 'http://www.heavens-above.com/orbitdisplay.aspx?icon=iss&width=400&height=400&satid=25544&uuid=' + \
                          str(uuid.uuid4())
                    bot.sendMessage(chat_id=chat_id,
                                    text='Watch for /' + watchedCommandName + ' has not changed.\n' +
                                         iss.format_iss_message(durationSeconds, requestText, startDateTime) + '\n' +
                                    url)
                if not main.AllWatchesContains(watchedCommandName, chat_id, message):
                    main.addToAllWatches(watchedCommandName, chat_id, message)
        else:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find the next ISS sighting for ' +
                                                  requestText.encode('utf-8') + '.')
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t find any places for ' +
                                              requestText.encode('utf-8') + '.')


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
