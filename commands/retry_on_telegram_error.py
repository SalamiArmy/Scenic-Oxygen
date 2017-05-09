# coding=utf-8
import sys
from time import sleep


def IsTooLongForCaption(text):
    return len(text) > 200


def SendDocumentWithRetry(bot, chat_id, imagelink, requestText):
    numberOfRetries = 5
    sendException = True
    while sendException and numberOfRetries > 0:
        try:
            caption_text = requestText + ': ' + imagelink.encode('utf-8') if not IsTooLongForCaption(requestText + ':' + imagelink) \
                else imagelink
            IsUrlTooLongForCaption = IsTooLongForCaption(caption_text)
            bot.sendDocument(chat_id=chat_id,
                             document=imagelink.encode('utf-8'),
                             filename=requestText.replace('.','').encode('utf-8'),
                             caption=(caption_text if not IsUrlTooLongForCaption else '').encode('utf-8'))
            if (IsUrlTooLongForCaption):
                print imagelink
            sendException = False
        except:
            sendException = True
            numberOfRetries -= 1
            print(sys.exc_info()[0])
            sleep(10)
    return numberOfRetries > 0


def SendPhotoWithRetry(bot, chat_id, imagelink, requestText):
    if imagelink[:4] == '.gif':
        return False
    numberOfRetries = 5
    sendException = True
    while sendException and numberOfRetries > 0:
        try:
            caption_text = requestText + ': ' + imagelink.encode('utf-8') if not IsTooLongForCaption(requestText + ':' + imagelink) \
                else imagelink
            IsUrlTooLongForCaption = IsTooLongForCaption(caption_text)
            bot.sendPhoto(chat_id=chat_id,
                          photo=imagelink.encode('utf-8'),
                          caption=(caption_text if not IsUrlTooLongForCaption else '').encode('utf-8'))
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