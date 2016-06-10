import string

import telegram


def SendDocumentWithRetry(bot, chat_id, imagelink, requestText):
    numberOfRetries = 6
    sendException = True
    while sendException and numberOfRetries > 0:
        try:
            bot.sendDocument(chat_id=chat_id, filename=requestText.encode('utf-8'), document=imagelink.encode('utf-8'))
            sendException = False
        except:
            sendException = True
            numberOfRetries -= 1
    return numberOfRetries > 0

def SendPhotoWithRetry(bot, chat_id, imagelink, captionText, user, intention_confidence=0.0):
    numberOfRetries = 6
    sendException = True
    while sendException and numberOfRetries > 0:
        try:
            bot.sendPhoto(chat_id=chat_id,
                          photo=imagelink.encode('utf-8'),
                          caption=(user + ': ' if not user == '' else '') + captionText.encode('utf-8') +
                                  (' ' + imagelink if len(imagelink) < 100 else '').encode('utf-8') +
                        '\nMight I add that I am ' + str(intention_confidence) + '% confident you wanted to see this.' if intention_confidence > 0.0 else '')
            sendException = False
        except:
            sendException = True
            numberOfRetries -= 1
    return numberOfRetries > 0