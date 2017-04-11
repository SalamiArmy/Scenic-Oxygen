import sys
from time import sleep

import threading


def IsTooLongForCaption(imagelink):
    return len(imagelink) > 200


def SendDocumentWithRetry(bot, chat_id, imagelink, requestText):
    numberOfRetries = 6
    sendException = True
    while sendException and numberOfRetries > 0:
        try:
            IsUrlTooLongForCaption = IsTooLongForCaption(requestText + ':' + imagelink)
            print("Trying to send " + imagelink)
            bot.sendDocument(chat_id, imagelink.encode('utf-8'), requestText.encode('utf-8'), (requestText + ':' + imagelink if not IsUrlTooLongForCaption else '').encode('utf-8'))
            if (IsUrlTooLongForCaption):
                print imagelink
            sendException = False
        except:
            sendException = True
            numberOfRetries -= 1
            print(sys.exc_info()[0])
            sleep(10)
    return numberOfRetries > 0


def SendPhotoWithRetry(bot, chat_id, imagelink, requestText, intention_confidence=0.0):
    if imagelink[:4] == '.gif':
        return False
    numberOfRetries = 6
    sendException = True
    while sendException and numberOfRetries > 0:
        try:
            IsUrlTooLongForCaption = IsTooLongForCaption(requestText + ':' + imagelink)
            print("Trying to send " + imagelink)
            bot.sendPhoto(chat_id=chat_id,
                          photo=imagelink.encode('utf-8'),
                          caption=(requestText + ':' + imagelink if not IsUrlTooLongForCaption else '').encode('utf-8') +
                                  ('\nMight I add that I am ' + str(intention_confidence) + '% confident you wanted to see this.' if intention_confidence > 0.0 else ''))
            if (IsUrlTooLongForCaption):
                print imagelink
            sendException = False
        except:
            sendException = True
            numberOfRetries -= 1
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            sleep(10)
    return not sendException and numberOfRetries > 0