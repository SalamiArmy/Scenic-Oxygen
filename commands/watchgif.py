# coding=utf-8
import string

import main
from commands import getgif
from commands import retry_on_telegram_error



def run(bot, chat_id, user, keyConfig, message, intention_confidence=0.0):
    requestText = message.replace(bot.name, "").strip()
    data = getgif.search_google_for_gifs(keyConfig, requestText)
    if 'items' in data and len(data['items']) >= 1:
        imagelink = data['items'][0]['link']
        print('got image links for ' + requestText + ' as ' + imagelink)
        if getgif.isGifAnimated(imagelink):
            if not getgif.wasPreviouslyAddedLink(chat_id, imagelink):
                getgif.addPreviouslySeenGifsValue(chat_id, imagelink)
                if user != 'Watcher':
                    bot.sendMessage(chat_id=chat_id, text='Now watching /' +
                                                          getgif.CommandName + ' ' + requestText + '.')
                    retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, user)
                else:
                    bot.sendMessage(chat_id=chat_id, text='Watched /' +
                                                          getgif.CommandName + ' ' + requestText + ' changed.')
                    retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, user)
            else:
                if user != 'Watcher':
                    bot.sendMessage(chat_id=chat_id, text=user + ', watch for /' +
                                                          getgif.CommandName + ' ' + requestText + ' has not changed.')
                    retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, user)
        else:
            if user != 'Watcher':
                bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      ', I\'m afraid gif is not animated.\n' + imagelink)
        if not main.AllWatchesContains(getgif.CommandName, chat_id, requestText):
            main.addToAllWatches(getgif.CommandName, chat_id, requestText)
    else:
        if user != 'Watcher':
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t watch ' +
                                                  'because I did not find enough results for /getgif ' +
                                                  string.capwords(requestText.encode('utf-8')))


def unwatch(bot, chat_id, message):
    watches = main.getAllWatches()
    if ',' + str(chat_id) + ':' + getgif.CommandName + ':' + message + ',' in watches or ',' + str(chat_id) + ':' + getgif.CommandName + ':' + message in watches:
        main.removeFromAllWatches(str(chat_id) + ':' + getgif.CommandName + ':' + message)
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + getgif.CommandName + ' ' + message + ' has been removed.')
    else:
        bot.sendMessage(chat_id=chat_id, text='Watch for /' + getgif.CommandName + ' ' + message + ' not found.')
    if getgif.getPreviouslySeenGifsValue(chat_id) != '':
        getgif.setPreviouslySeenGifsValue(chat_id, '')
