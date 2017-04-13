# coding=utf-8
import random
import urllib

import xmltodict


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    bot.sendMessage(chat_id=chat_id, text=get_define_data(keyConfig, user, requestText))

def get_define_data(keyConfig, user, requestText):
    dicUrl = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/'
    realUrl = dicUrl + requestText.encode('utf-8').replace('?', '').replace('&', '') + '?key=' + keyConfig.get('Merriam-Webster', 'API_KEY')
    getXml = urllib.urlopen(realUrl).read()
    if not getXml or 'invalid' in getXml.lower():
        return False
    data = xmltodict.parse(getXml)
    getAllEntries = data['entry_list']
    if len(getAllEntries) >= 1 and 'entry' in getAllEntries:
        if 'suggestion' not in getAllEntries:
            getEntry = getAllEntries['entry']
            if type(getEntry) is list:
                entry = getEntry[random.randint(0, len(getEntry) - 1)]
            else:
                entry = getEntry
            formatted_entry = format_entry(entry, user, requestText)
            if formatted_entry:
                return formatted_entry
        else:
            return 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
                   ', I\'m afraid I can\'t find any definitions for the word ' +\
                   requestText + '. Did you mean ' + ' '.join(getAllEntries['suggestion']) + '?'
    else:
        return 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
               ', I\'m afraid I can\'t find any definitions for the word ' + requestText + '.'


def format_entry(entry, user, requestText):
    if 'fl' in entry:
        partOfSpeech = entry['fl']
        if len(partOfSpeech) >= 1:
            getAllDefs = entry['def']['dt']
            getDefinition = ''
            count = 0
            while getDefinition == '' or count > len(getAllDefs):
                if type(getAllDefs) is list:
                    getDefinition = getAllDefs[count]
                else:
                    getDefinition = getAllDefs
                if '#text' in getDefinition:
                    definitionText = getDefinition['#text']
                else:
                    definitionText = getDefinition
                definitionText = definitionText.replace(':', '').strip()
                count += 1
            if 'sound' in entry:
                soundFilename = entry['sound']['wav']
                soundUrl = 'http://media.merriam-webster.com/soundc11/' + str(soundFilename[:1]) + '/' + str(soundFilename)
                return (user + ': ' if not user == '' else '') + requestText.title() + "\n" + partOfSpeech + ".\n\n" + definitionText + '\n' + soundUrl

    elif 'cx' in entry:
        return (user + ': ' if not user == '' else '') + requestText.title() + ":\n" + entry['cx']['cl'] + ' ' + entry['ew']
    else:
        return ''


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