# coding=utf-8
import string
import urllib
import io

from google.appengine.ext import ndb

import sys
from PIL import Image

from commands import retry_on_telegram_error
from commands import get

CommandName = 'getgif'

class SeenGifs(ndb.Model):
    # key name: getgif:str(chat_id)
    allPreviousSeenGifs = ndb.StringProperty(indexed=False, default='')


# ================================

def setPreviouslySeenGifsValue(chat_id, NewValue):
    es = SeenGifs.get_or_insert(CommandName + ':' + str(chat_id))
    es.allPreviousSeenGifs = NewValue.encode('utf-8')
    es.put()

def addPreviouslySeenGifsValue(chat_id, NewValue):
    es = SeenGifs.get_or_insert(CommandName + ':' + str(chat_id))
    if es.allPreviousSeenGifs == '':
        es.allPreviousSeenGifs = NewValue.encode('utf-8')
    else:
        es.allPreviousSeenGifs += ',' + NewValue.encode('utf-8')
    es.put()

def getPreviouslySeenGifsValue(chat_id):
    es = SeenGifs.get_or_insert(CommandName + ':' + str(chat_id))
    if es:
        return es.allPreviousSeenGifs.encode('utf-8')
    return ''

def wasPreviouslySeenGif(chat_id, gif_link):
    allPreviousLinks = getPreviouslySeenGifsValue(chat_id)
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
            'searchType': "image",
            'safe': "off",
            'q': requestText,
            'fileType': 'gif',
            'start': 1}
    if totalResults > 1:
        Send_Animated_Gifs(bot, chat_id, user, requestText, args, totalResults)
    else:
        Send_First_Animated_Gif(bot, chat_id, user, requestText, args)


def isGifAnimated(imagelink):
    global gif, image_file, fd
    try:
        fd = urllib.urlopen(imagelink)
        image_file = io.BytesIO(fd.read())
        gif = Image.open(image_file)
    except IOError:
        try:
            if gif:
                gif.fp.close()
            if image_file:
                image_file.close()
            if fd:
                fd.close()
        except UnboundLocalError:
            print("gif, image_file or fd local not defined")
        except NameError:
            print("gif, image_file or fd global not defined")
        return False
    else:
        try:
            gif.seek(1)
        except EOFError:
            try:
                if gif:
                    gif.fp.close()
                if image_file:
                    image_file.close()
                if fd:
                    fd.close()
            except UnboundLocalError:
                print("gif, image_file or fd local not defined")
            except NameError:
                print("gif, image_file or fd global not defined")
            return False
        else:
            return int(sys.getsizeof(image_file)) < 10000000


def Send_First_Animated_Gif(bot, chat_id, user, requestText, args):
    data, total_results, results_this_page = get.Google_Custom_Search(args)
    total_results = total_results if total_results < 1000 else 1000
    if 'items' in data and total_results > 0:
        total_offset = 0
        thereWasAnError = True
        while thereWasAnError and int(total_offset) < int(total_results):
            offset_this_page = 0
            while thereWasAnError and int(offset_this_page) < int(results_this_page):
                imagelink = data['items'][offset_this_page]['link']
                offset_this_page += 1
                total_offset += 1
                if '?' in imagelink:
                    imagelink = imagelink[:imagelink.index('?')]
                if not wasPreviouslySeenGif(chat_id, imagelink):
                    if isGifAnimated(imagelink):
                        thereWasAnError = not retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, requestText)
                    addPreviouslySeenGifsValue(chat_id, imagelink)
            if thereWasAnError:
                args['start'] = total_offset+1
                data, total_results, results_this_page = get.Google_Custom_Search(args)
        if thereWasAnError or not total_offset < total_results:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find a gif for ' +
                                                  string.capwords(requestText.encode('utf-8')) + '.'.encode('utf-8'))
        else:
            return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t find a gif for ' +
                                              string.capwords(requestText.encode('utf-8')) + '.'.encode('utf-8'))

def Send_Animated_Gifs(bot, chat_id, user, requestText, args, totalResults):
    data, total_results, results_this_page = get.Google_Custom_Search(args)
    total_results = total_results if total_results < 1000 else 1000
    if 'items' in data and total_results > 0:
        total_offset = 0
        total_sent = 0
        while int(total_sent) < int(totalResults):
            offset_this_page = 0
            while int(total_sent) < int(totalResults) and int(offset_this_page) < int(results_this_page):
                imagelink = data['items'][offset_this_page]['link']
                offset_this_page += 1
                total_offset += 1
                if '?' in imagelink:
                    imagelink = imagelink[:imagelink.index('?')]
                if not wasPreviouslySeenGif(chat_id, imagelink):
                    if isGifAnimated(imagelink):
                        if retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, requestText + ' ' + str(total_sent+1)):
                            total_sent += 1
                            print('sent gif number ' + str(total_sent))
                    addPreviouslySeenGifsValue(chat_id, imagelink)
            if int(total_sent) < int(totalResults):
                args['start'] = total_offset+1
                data, total_results, results_this_page = get.Google_Custom_Search(args)
        if int(total_sent) < int(totalResults):
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find any more gifs for ' +
                                                  string.capwords(requestText.encode('utf-8')) + '.'.encode('utf-8'))
        else:
            return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t find a gif for ' +
                                              string.capwords(requestText.encode('utf-8')) + '.'.encode('utf-8'))

