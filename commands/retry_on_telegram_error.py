import telegram


def SendDocumentWithRetry(bot, chat_id, imagelink, requestText):
    numberOfRetries = 6
    sendException = True
    while sendException and numberOfRetries > 0:
        try:
            bot.sendDocument(chat_id=chat_id,
                             filename=requestText.encode('utf-8'),
                             document=imagelink.encode('utf-8'))
            sendException = False
        except telegram.TelegramError:
            sendException = True
            numberOfRetries -= 1