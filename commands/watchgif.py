# coding=utf-8
import string

from google.appengine.ext import ndb

import main
from commands import getgif
from commands import retry_on_telegram_error

watchedCommandName = 'getgif'


class WatchValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')
    allPreviousAddedLinks = ndb.StringProperty(indexed=False, default='')


# ================================

def setWatchValue(chat_id, request, NewValue):
    es = WatchValue.get_or_insert(watchedCommandName + ':' + str(chat_id) + ':' + request)
    es.currentValue = NewValue
    es.put()

def addPreviouslyAddedLinkValue(chat_id, NewValue):
    es = WatchValue.get_or_insert(watchedCommandName + ':' + str(chat_id))
    if (es.allPreviousAddedLinks != ''):
        es.allPreviousAddedLinks += '\n' + NewValue
    else:
        es.allPreviousAddedLinks += NewValue
    es.put()


def getWatchValue(chat_id, request):
    es = WatchValue.get_by_id(watchedCommandName + ':' + str(chat_id) + ':' + request)
    if es:
        return es.currentValue
    return ''

def getPreviouslyAddedLinksValue(chat_id):
    es = WatchValue.get_by_id(watchedCommandName + ':' + str(chat_id))
    if es:
        return es.allPreviousAddedLinks.encode('utf-8')
    return ''

def wasPreviouslyAddedLink(chat_id, gif_link):
    allPreviousLinks = getPreviouslyAddedLinksValue(chat_id)
    if '\n' + gif_link + '\n' in allPreviousLinks or \
        allPreviousLinks.startswith(gif_link + '\n') or  \
        allPreviousLinks.endswith('\n' + gif_link) or  \
        allPreviousLinks == gif_link:
        return True;
    return False;

def is_new_gif(chat_id, gif_link):
    return gif_link not in getPreviouslyAddedLinksValue(chat_id)


def run(bot, chat_id, user, keyConfig, message, intention_confidence=0.0):
    requestText = message.replace(bot.name, "").strip()
    data = getgif.search_google_for_gifs(keyConfig, requestText)
    if 'items' in data and len(data['items']) >= 2:
        OldValue = getWatchValue(chat_id, requestText)
        imagelink = data['items'][0]['link']
        new_gif = is_new_gif(chat_id, imagelink)
        print('got image links for ' + requestText + ' as ' + imagelink)
        if getgif.isGifAnimated(imagelink):
            if OldValue != imagelink:
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
        if new_gif:
            bot.sendMessage(chat_id=chat_id, text='This is a new new gif!')

        if OldValue != imagelink:
            print('Setting watch value to ' + imagelink)
            setWatchValue(chat_id, requestText, imagelink)
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
    if getWatchValue(chat_id, message) != '':
        setWatchValue(chat_id, message, '')
