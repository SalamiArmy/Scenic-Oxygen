# coding=utf-8
import ConfigParser
import os
import urllib

import telegram
import xmltodict

#reverse image search imports:


def run(thorin, update):
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(os.getenv("THORIN_API_TOKEN"))

    # chat_id is required to reply to any message
    chat_id = update.message.chat_id
    message = update.message.text
    user = update.message.from_user.username \
        if not update.message.from_user.username == '' \
        else update.message.from_user.first_name + (' ' + update.message.from_user.last_name) \
        if not update.message.from_user.last_name == '' \
        else ''

    message = message.replace(bot.name, "").strip()

    splitText = message.split(' ', 1)

    requestText = splitText[1] if ' ' in message else ''


    dicUrl = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/'
    realUrl = dicUrl + requestText.encode('utf-8') + '?key=' + keyConfig.get('Merriam-Webster', 'API_KEY')
    data = xmltodict.parse(urllib.urlopen(realUrl).read())
    if len(data['entry_list']) >= 1:
        partOfSpeech = data['entry_list']['entry']['fl']
        if len(partOfSpeech) >= 1:
            definitionText = data['entry_list']['entry']['def']['dt'][0]
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            urlForCurrentChatAction = (user + ': ' if not user == '' else '') + \
                                      requestText.title() + ":\n" + \
                                      partOfSpeech + ".\n\n" + definitionText
            bot.sendMessage(chat_id=chat_id, text=urlForCurrentChatAction)
        else:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                                  ', I\'m afraid I can\'t find any definitions for the word ' + \
                                                  requestText + '.')
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I can\'t find any definitions for the word ' + \
                                  requestText + '.'
        bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)

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