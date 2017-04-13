# coding=utf-8
import json
import string
import urllib

from google.appengine.ext import ndb

from commands import retry_on_telegram_error

CommandName = 'get'

class SeenImages(ndb.Model):
    # key name: get:str(chat_id)
    allPreviousSeenImages = ndb.StringProperty(indexed=False, default='')


# ================================

def setPreviouslySeenImagesValue(chat_id, NewValue):
    es = SeenImages.get_or_insert(CommandName + ':' + str(chat_id))
    es.allPreviousSeenImages = NewValue.encode('utf-8')
    es.put()

def addPreviouslySeenImagesValue(chat_id, NewValue):
    es = SeenImages.get_or_insert(CommandName + ':' + str(chat_id))
    if es.allPreviousSeenImages == '':
        es.allPreviousSeenImages = NewValue.encode('utf-8')
    else:
        es.allPreviousSeenImages += ',' + NewValue.encode('utf-8')
    es.put()

def getPreviouslySeenImagesValue(chat_id):
    es = SeenImages.get_or_insert(CommandName + ':' + str(chat_id))
    if es:
        return es.allPreviousSeenImages.encode('utf-8')
    return ''

def wasPreviouslySeenImage(chat_id, gif_link):
    allPreviousLinks = getPreviouslySeenImagesValue(chat_id)
    if ',' + gif_link + ',' in allPreviousLinks or \
            allPreviousLinks.startswith(gif_link + ',') or  \
            allPreviousLinks.endswith(',' + gif_link) or  \
            allPreviousLinks == gif_link:
        return True
    return False

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    args = {'cx': keyConfig.get('Google', 'GCSE_SE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': 'image',
            'safe': 'off',
            'q': requestText,
            'start': 1}
    if totalResults > 1:
        Send_Images(bot, chat_id, user, requestText, args, totalResults)
    else:
        Send_First_Valid_Image(bot, chat_id, user, requestText, args)


def Google_Custom_Search(args):
    googurl = 'https://www.googleapis.com/customsearch/v1'
    realUrl = googurl + '?' + urllib.urlencode(args)
    data = json.load(urllib.urlopen(realUrl))
    total_results = 0
    results_this_page = 0
    if 'searchInformation' in data and 'totalResults' in data['searchInformation']:
        total_results = data['searchInformation']['totalResults']
    if 'queries' in data and 'request' in data['queries'] and len(data['queries']['request']) > 0 and 'count' in data['queries']['request'][0]:
        results_this_page = data['queries']['request'][0]['count']
    return data, total_results, results_this_page

def Send_First_Valid_Image(bot, chat_id, user, requestText, args):
    data, total_results, results_this_page = Google_Custom_Search(args)
    if 'items' in data and total_results > 0:
        total_offset = 0
        thereWasAnError = True
        while thereWasAnError and total_offset < total_results:
            offset_this_page = 0
            while thereWasAnError and offset_this_page < results_this_page:
                imagelink = data['items'][offset_this_page]['link']
                offset_this_page += 1
                total_offset += 1
                if '?' in imagelink:
                    imagelink = imagelink[:imagelink.index('?')]
                if not imagelink.startswith('x-raw-image:///') and imagelink != '' and not wasPreviouslySeenImage(chat_id, imagelink):
                    thereWasAnError = not retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink, requestText)
                addPreviouslySeenImagesValue(chat_id, imagelink)
            if thereWasAnError:
                args['start'] = total_offset+1
                data, total_results, results_this_page = Google_Custom_Search(args)
        if (thereWasAnError or not total_offset < total_results):
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find any images for ' +
                                                  string.capwords(requestText.encode('utf-8')))
        else:
            return True
    else:
        if 'error' in data:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  data['error']['message'])
        else:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find any images for ' +
                                                  string.capwords(requestText.encode('utf-8')))

def Send_Images(bot, chat_id, user, requestText, args, number):
    data, total_results, results_this_page = Google_Custom_Search(args)
    if 'items' in data and total_results > 0:
        total_offset = 0
        total_sent = 0
        while total_sent < number and total_offset < total_results:
            offset_this_page = 0
            while total_sent < number and offset_this_page < results_this_page:
                imagelink = data['items'][offset_this_page]['link']
                offset_this_page += 1
                total_offset += 1
                if '?' in imagelink:
                    imagelink = imagelink[:imagelink.index('?')]
                if not imagelink.startswith('x-raw-image:///') and imagelink != '' and not wasPreviouslySeenImage(chat_id, imagelink):
                    if not retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink, requestText):
                        total_sent += 1
                addPreviouslySeenImagesValue(chat_id, imagelink)
            if total_sent < number:
                args['start'] = total_offset+1
                data, total_results, results_this_page = Google_Custom_Search(args)
        if (total_sent < number or not total_offset < total_results):
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find any more images for ' +
                                                  string.capwords(requestText.encode('utf-8')))
        else:
            return True
    else:
        if 'error' in data:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  data['error']['message'])
        else:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find any images for ' +
                                                  string.capwords(requestText.encode('utf-8')))
