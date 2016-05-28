# coding=utf-8
import ConfigParser
import urllib

import telegram
import xmltodict


def run(chat_id, user, message):
    # Read keys.ini file should be at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    requestText = message.replace(bot.name, "").strip()

    dicUrl = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/'
    realUrl = dicUrl + requestText.encode('utf-8') + '?key=' + keyConfig.get('Merriam-Webster', 'API_KEY')
    data = xmltodict.parse(urllib.urlopen(realUrl).read())
    if len(data['entry_list']) >= 1:
        partOfSpeech = data['entry_list']['entry']['fl']
        if len(partOfSpeech) >= 1:
            definitionText = data['entry_list']['entry']['def']['dt'][0]
            urlForCurrentChatAction = (user + ': ' if not user == '' else '') + \
                                      requestText.title() + ":\n" + \
                                      partOfSpeech + ".\n\n" + definitionText
            bot.sendMessage(chat_id=chat_id, text=urlForCurrentChatAction)
        else:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                                  ', I\'m afraid I can\'t find any definitions for the word ' + \
                                                  requestText + '.')
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find any definitions for the word ' + \
                                              requestText + '.')

        ############################# Ashley: http://dictionaryapi.net/ is down! ###############################
        # dicUrl = 'http://dictionaryapi.net/api/definition/'
        # realUrl = dicUrl + requestText.encode('utf-8')
        # data = json.load(urllib.urlopen(realUrl))
        # if len(data) >= 1:
        #     partOfSpeech = data[random.randint(0, len(data) - 1)]
        #     if len(partOfSpeech['Definitions']) >= 1:
        #         definitionText = partOfSpeech['Definitions'][0]
        #         bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        #         userWithCurrentChatAction = chat_id
        #         urlForCurrentChatAction = (user + ': ' if not user == '' else '') +\
        #                                   requestText.title() + ":\n" + \
        #                                   partOfSpeech['PartOfSpeech'] + ".\n\n" + definitionText
        #         bot.sendMessage(chat_id=chat_id, text=urlForCurrentChatAction)
        #     else:
        #         bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        #         userWithCurrentChatAction = chat_id
        #         urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
        #                                   ', I\'m afraid I can\'t find any definitions for the word ' +\
        #                                   requestText + '.'
        #         bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)
        # else:
        #     bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        #     userWithCurrentChatAction = chat_id
        #     urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
        #                               ', I\'m afraid I can\'t find any definitions for the word ' +\
        #                               requestText + '.'
        #     bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)