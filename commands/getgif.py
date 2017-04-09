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

class WatchValue(ndb.Model):
    # key name: getgif:str(chat_id)
    allPreviousSeenGifs = ndb.StringProperty(indexed=False, default='')


# ================================

def setPreviouslySeenGifsValue(chat_id, request, NewValue):
    es = WatchValue.get_or_insert(CommandName + ':' + str(chat_id) + ':' + request)
    es.allPreviousSeenGifs = NewValue
    es.put()

def addPreviouslySeenGifsValue(chat_id, request, NewValue):
    es = WatchValue.get_or_insert(CommandName + ':' + str(chat_id) + ':' + request)
    if es.allPreviousSeenGifs == '':
        es.allPreviousSeenGifs = NewValue
    else:
        es.allPreviousSeenGifs += ',' + NewValue
    es.put()

def getPreviouslySeenGifsValue(chat_id):
    es = WatchValue.get_by_id(CommandName + ':' + str(chat_id))
    if es:
        return es.allPreviousSeenGifs.encode('utf-8')
    return ''

def wasPreviouslyAddedLink(chat_id, gif_link):
    allPreviousLinks = getPreviouslySeenGifsValue(chat_id)
    if '\n' + gif_link + '\n' in allPreviousLinks or \
        allPreviousLinks.startswith(gif_link + '\n') or  \
        allPreviousLinks.endswith('\n' + gif_link) or  \
        allPreviousLinks == gif_link:
        return True;
    return False;


def run(bot, chat_id, user, keyConfig, message):
    global gif
    requestText = message.replace(bot.name, "").strip()

    data = search_google_for_gifs(keyConfig, requestText)
    offset = 0
    thereWasAnError = True
    if 'items' in data and len(data['items']) >= 1:
        items_length_limit = 9
        item_count = items_length_limit if len(data['items'])>=items_length_limit else len(data['items'])
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        while thereWasAnError and offset < item_count:
            imagelink = data['items'][offset]['link']
            offset += 1
            if '?' in imagelink:
                imagelink = imagelink[:imagelink.index('?')]
            thereWasAnError = not isGifAnimated(imagelink)
            if not wasPreviouslyAddedLink(chat_id, imagelink):
                addPreviouslySeenGifsValue(chat_id, imagelink)
            else:
                thereWasAnError = True
            if not thereWasAnError:
                thereWasAnError = not retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, requestText)
        if thereWasAnError or not offset < 9:
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
            if (getsizeof > 10000):
                print("...gif is larger than limit of 10000000 bytes, file size appears to be " + str(getsizeof) + ' bytes')
                return False
            else:
                print("...gif under size limit of 10000000 bytes, file size appears to be " + str(getsizeof) + ' bytes')
    return True


def search_google_for_gifs(keyConfig, requestText):
    googurl = 'https://www.googleapis.com/customsearch/v1'
    args = {'cx': keyConfig.get('Google', 'GCSE_SE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': "image",
            'safe': "off",
            'q': requestText,
            'fileType': 'gif'}
    realUrl = googurl + '?' + urllib.urlencode(args)
    data = json.load(urllib.urlopen(realUrl))
    return data

