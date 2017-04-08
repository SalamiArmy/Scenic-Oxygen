# coding=utf-8
import string

from google.appengine.ext import ndb

import main
from commands import getgif
from commands import retry_on_telegram_error

watchedCommandName = 'getgif'


class WatchValue(ndb.Model):
    # key name: getgif:str(chat_id)
    allPreviousSeenGifs = ndb.StringProperty(indexed=False, default='')


# ================================

def setPreviouslySeenGifsValue(chat_id, request, NewValue):
    es = WatchValue.get_or_insert(watchedCommandName + ':' + str(chat_id) + ':' + request)
    es.allPreviousSeenGifs = NewValue
    es.put()

def addPreviouslySeenGifsValue(chat_id, request, NewValue):
    es = WatchValue.get_or_insert(watchedCommandName + ':' + str(chat_id) + ':' + request)
    if es.allPreviousSeenGifs == '':
        es.allPreviousSeenGifs = NewValue
    else:
        es.allPreviousSeenGifs += ',' + NewValue
    es.put()

def getPreviouslySeenGifsValue(chat_id):
    es = WatchValue.get_by_id(watchedCommandName + ':' + str(chat_id))
    if es:
        return es.allPreviousSeenGifs.encode('utf-8')
    return ''

def wasPreviouslyAddedLink(chat_id, gif_link):
    allPreviousLinks = getPreviouslySeenGifsValue(chat_id)
    if '\n' + gif_link + '\n' in allPreviousLinks or \
        allPreviousLinks.startswith(gif_link + '\n') or  \
        allPreviousLinks.endswith('\n' + gif_link) or  \
        allPreviousLinks == gif_link:
        return True;
    return False;


def run(bot, chat_id, user, keyConfig, message, intention_confidence=0.0):
    requestText = message.replace(bot.name, "").strip()
    data = getgif.search_google_for_gifs(keyConfig, requestText)
    if 'items' in data and len(data['items']) >= 1:
        imagelink = data['items'][0]['link']
        print('got image links for ' + requestText + ' as ' + imagelink)
        if getgif.isGifAnimated(imagelink):
            if not wasPreviouslyAddedLink(chat_id, imagelink):
                addPreviouslySeenGifsValue(chat_id, imagelink)
                if user != 'Watcher':
                    bot.sendMessage(chat_id=chat_id, text='Now watching /' +
                                                          watchedCommandName + ' ' + requestText + '.')
                    retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, user)
                else:
                    bot.sendMessage(chat_id=chat_id, text='Watched /' +
                                                          watchedCommandName + ' ' + requestText + ' changed.')
                    retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, user)
            else:
                if user != 'Watcher':
                    bot.sendMessage(chat_id=chat_id, text=user + ', watch for /' +
                                                          watchedCommandName + ' ' + requestText + ' has not changed.')
                    retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, user)
        else:
            if user != 'Watcher':
                bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      ', I\'m afraid gif is not animated.\n' + imagelink)
        if not main.AllWatchesContains(watchedCommandName, chat_id, requestText):
            main.addToAllWatches(watchedCommandName, chat_id, requestText)
    else:
        if user != 'Watcher':
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t watch ' +
                                                  'because I did not find enough results for /getgif ' +
                                                  string.capwords(requestText.encode('utf-8')))


def unwatch(bot, chat_id, message):
    watches = main.getAllWatches()
    if ',' + str(chat_id) + ':' + watchedCommandName + ':' + message + ',' in watches or ',' + str(chat_id) + ':' + watchedCommandName + ':' + message in watches:
        main.removeFromAllWatches(str(chat_id) + ':' + watchedCommandName + ':' + message)
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' has been removed.')
    else:
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + watchedCommandName + ' ' + message + ' not found.')
    if getPreviouslySeenGifsValue(chat_id) != '':
        setPreviouslySeenGifsValue(chat_id, '')
