# coding=utf-8

from google.appengine.ext import ndb

from commands import get

CommandName = 'getxxx'

class SeenXXX(ndb.Model):
    # key name: get:str(chat_id)
    allPreviousSeenXXX = ndb.StringProperty(indexed=False, default='')


# ================================

def setPreviouslySeenXXXValue(chat_id, NewValue):
    es = SeenXXX.get_or_insert(CommandName + ':' + str(chat_id))
    es.allPreviousSeenXXX = NewValue.encode('utf-8')
    es.put()

def addPreviouslySeenXXXValue(chat_id, NewValue):
    es = SeenXXX.get_or_insert(CommandName + ':' + str(chat_id))
    if es.allPreviousSeenXXX == '':
        es.allPreviousSeenXXX = NewValue.encode('utf-8')
    else:
        es.allPreviousSeenXXX += ',' + NewValue.encode('utf-8')
    es.put()

def getPreviouslySeenXXXValue(chat_id):
    es = SeenXXX.get_or_insert(CommandName + ':' + str(chat_id))
    if es:
        return es.allPreviousSeenXXX.encode('utf-8')
    return ''

def wasPreviouslySeenXXX(chat_id, xxx_link):
    allPreviousLinks = getPreviouslySeenXXXValue(chat_id)
    if ',' + xxx_link + ',' in allPreviousLinks or \
            allPreviousLinks.startswith(xxx_link + ',') or  \
            allPreviousLinks.endswith(',' + xxx_link) or  \
            allPreviousLinks == xxx_link:
        return True
    return False


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    args, data, results_this_page, total_results = search_gcse_for_xxx(keyConfig, requestText)
    if totalResults > 1:
        Send_XXXs(bot, chat_id, user, requestText, data, total_results, results_this_page, totalResults, args)
    else:
        Send_First_Valid_XXX(bot, chat_id, user, requestText, data, total_results, results_this_page)


def search_gcse_for_xxx(keyConfig, requestText):
    args = {'cx': keyConfig.get('Google', 'GCSE_XSE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'safe': 'off',
            'q': requestText,
            'start': 1}
    data, total_results, results_this_page = get.Google_Custom_Search(args)
    return args, data, results_this_page, total_results


def Send_First_Valid_XXX(bot, chat_id, user, requestText, data, total_results, results_this_page):
    if data['searchInformation']['totalResults'] >= '1':
        sent_count = 0
        for item in data['items']:
            xlink = item['link']
            if is_valid_xxx(xlink):
                if not wasPreviouslySeenXXX(chat_id, xlink):
                    bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') + xlink)
                    addPreviouslySeenXXXValue(chat_id, xlink)
                    sent_count += 1
                    break
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', you\'re just too filthy.')


def is_valid_xxx(xlink):
    return 'xvideos.com/tags/' not in xlink and \
           'xvideos.com/favorite/' not in xlink and \
           'xvideos.com/?k=' not in xlink and \
           'xvideos.com/tags' not in xlink and \
           'pornhub.com/users/' not in xlink and \
           'pornhub.com/video/search?search=' not in xlink and \
           'pornhub.com/insights/' not in xlink and \
           'pornhub.com/devices/' not in xlink and \
           'pornhub.com/gay/' not in xlink and \
           'pornhub.com/pornstar/' not in xlink and \
           'xvideos.com/profiles/' not in xlink and \
           'xnxx.com/?' not in xlink and \
           'xnxx.com/tags/' not in xlink and \
           'xhamster.com/stories_search' not in xlink and \
           'redtube.com/pornstar/' not in xlink and \
           'search?search=' not in xlink and \
           'xhamster.com/forums/' not in xlink and \
           'xvideos.com/profiles/' not in xlink


def Send_XXXs(bot, chat_id, user, requestText, data, total_results, results_this_page, number, args):
    if data['searchInformation']['totalResults'] >= '1':
        sent_count = 0
        total_offset = 0
        while int(sent_count) < int(number) and int(total_offset) < int(total_results):
            for item in data['items']:
                xlink = item['link']
                total_offset += 1
                if is_valid_xxx(xlink):
                    if not wasPreviouslySeenXXX(chat_id, xlink):
                        bot.sendMessage(chat_id=chat_id, text=requestText + ' ' + str(sent_count+1)
                                                              + ' of ' + str(number) + ':' + xlink)
                        addPreviouslySeenXXXValue(chat_id, xlink)
                        sent_count += 1
                if int(sent_count) >= int(number) or int(total_offset) >= int(total_results):
                    break
            if int(sent_count) < int(number) and int(total_offset) < int(total_results):
                args['start'] = total_offset+1
                data, total_results, results_this_page = get.Google_Custom_Search(args)
        if int(sent_count) < int(number):
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I cannot find enough filth for ' + requestText + '.' +
                                                  ' I could only find ' + str(sent_count) + ' out of ' + str(number))
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', you\'re just too filthy.')
