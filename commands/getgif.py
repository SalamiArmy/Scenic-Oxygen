# coding=utf-8
import json
import string
import urllib
import io
from google.appengine.ext import ndb

import sys
from PIL import Image

import telegram

from commands import retry_on_telegram_error

CommandName = 'getgif'

class GifWatchValue(ndb.Model):
    # key name: getgif:str(chat_id)
    allPreviousSeenGifs = ndb.StringProperty(indexed=False, default='')


# ================================

def setPreviouslySeenGifsValue(chat_id, NewValue):
    es = GifWatchValue.get_or_insert(CommandName + ':' + str(chat_id))
    es.allPreviousSeenGifs = NewValue.encode('utf-8')
    es.put()

def addPreviouslySeenGifsValue(chat_id, NewValue):
    es = GifWatchValue.get_or_insert(CommandName + ':' + str(chat_id))
    if es.allPreviousSeenGifs == '':
        es.allPreviousSeenGifs = NewValue.encode('utf-8')
    else:
        es.allPreviousSeenGifs += ',' + NewValue.encode('utf-8')
    es.put()

def getPreviouslySeenGifsValue(chat_id):
    es = GifWatchValue.get_by_id(CommandName + ':' + str(chat_id))
    if es:
        return es.allPreviousSeenGifs.encode('utf-8')
    return ''

def wasPreviouslyAddedLink(chat_id, gif_link):
    allPreviousLinks = getPreviouslySeenGifsValue(chat_id)
    if ',' + gif_link + ',' in allPreviousLinks or \
        allPreviousLinks.startswith(gif_link + ',') or  \
        allPreviousLinks.endswith(',' + gif_link) or  \
        allPreviousLinks == gif_link:
        return True
    return False


def run(bot, chat_id, user, keyConfig, message):
    requestText = message.replace(bot.name, "").strip()
    data, total_results, results_this_page = search_google_for_gifs(keyConfig, requestText)
    total_offset = 0
    if 'items' in data and total_results > 0:
        items_length_limit = 20
        thereWasAnError = True
        while total_offset < (total_results if total_results < items_length_limit else items_length_limit):
            offset_this_page = 0
            while thereWasAnError and offset_this_page < results_this_page:
                imagelink = data['items'][offset_this_page]['link']
                offset_this_page += 1
                total_offset += 1
                if '?' in imagelink:
                    imagelink = imagelink[:imagelink.index('?')]
                if not wasPreviouslyAddedLink(chat_id, imagelink) and isGifAnimated(imagelink):
                    thereWasAnError = not retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, requestText)
                    addPreviouslySeenGifsValue(chat_id, imagelink)
                else:
                    thereWasAnError = True
            data, total_results, results_this_page = search_google_for_gifs(keyConfig, requestText, total_offset+1)
        if thereWasAnError or not total_offset < items_length_limit:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find a gif for ' +
                                                  string.capwords(requestText.encode('utf-8')) + '.'.encode('utf-8'))
        else:
            return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t find a gif for ' +
                                              string.capwords(requestText.encode('utf-8')) + '.'.encode('utf-8'))


def isGifAnimated(imagelink):
    global gif, image_file, fd
    print("Openning url " + imagelink)
    try:
        fd = urllib.urlopen(imagelink)
        print("Reading gif...")
        image_file = io.BytesIO(fd.read())
        print("Parsing gif...")
        gif = Image.open(image_file)
    except IOError:
        gif.fp.close()
        image_file.close()
        fd.close()
        print("...not a gif")
        return False
    else:
        try:
            print("Checking gif for animation...")
            gif.seek(1)
        except EOFError:
            gif.fp.close()
            image_file.close()
            fd.close()
            print("...not animated")
            return False
        else:
            print("...gif is animated, confirmed! Checking file size...")
            getsizeof = sys.getsizeof(image_file)
            size_limit = 10000000
            if (len(str(getsizeof)) > 7):
                print('...gif is larger than limit of ' + str(size_limit) + ' bytes, file size appears to be ' + str(getsizeof) + ' bytes')
                return False
            else:
                print('...gif under size limit of ' + str(size_limit) + ' bytes, file size appears to be ' + str(getsizeof) + ' bytes')
    return True


def search_google_for_gifs(keyConfig, requestText, startIndex=1):
    googurl = 'https://www.googleapis.com/customsearch/v1'
    args = {'cx': keyConfig.get('Google', 'GCSE_SE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': "image",
            'safe': "off",
            'q': requestText,
            'fileType': 'gif',
            'start': startIndex}
    realUrl = googurl + '?' + urllib.urlencode(args)
    data = json.load(urllib.urlopen(realUrl))
    total_results = 0
    results_this_page = 0
    if 'searchInformation' in data and 'totalResults' in data['searchInformation']:
        total_results = data['searchInformation']['totalResults']
    if 'queries' in data and 'request' in data['queries'] and len(data['queries']['request']) > 0 and 'count' in data['queries']['request'][0]:
        results_this_page = data['queries']['request'][0]['count']
    return data, total_results, results_this_page
