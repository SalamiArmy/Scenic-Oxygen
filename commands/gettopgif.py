# coding=utf-8
import json
import urllib2

from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from commands import retry_on_telegram_error
from commands import getgif

watchedCommandName = 'gettopgif'


class WatchValue(ndb.Model):
    # key name: str(chat_id)
    currentValue = ndb.StringProperty(indexed=False, default='')
    all_chat_ids = ndb.StringProperty(indexed=False, default='')


# ================================

def setWatchValue(chat_id, NewValue):
    es = WatchValue.get_or_insert(watchedCommandName + ':' + str(chat_id))
    es.currentValue = NewValue
    es.put()


def getWatchValue(chat_id):
    es = WatchValue.get_by_id(watchedCommandName + ':' + str(chat_id))
    if es:
        return es.currentValue
    return ''

def addToAllWatches(chat_id):
    es = WatchValue.get_or_insert(watchedCommandName + ':' + 'AllWatchers')
    es.all_chat_ids += ',' + str(chat_id)
    es.put()

def AllWatchesContains(chat_id):
    es = WatchValue.get_by_id(watchedCommandName + ':' + 'AllWatchers')
    if es:
        return (',' + str(chat_id)) in str(es.all_chat_ids) or \
               (str(chat_id) + ',') in str(es.all_chat_ids)
    return False

def setAllWatchesValue(NewValue):
    es = WatchValue.get_or_insert(watchedCommandName + ':' + 'AllWatchers')
    es.all_chat_ids = NewValue
    es.put()

def getAllWatches():
    es = WatchValue.get_by_id(watchedCommandName + ':' + 'AllWatchers')
    if es:
        return es.all_chat_ids
    return ''

def removeFromAllWatches(watch):
    setAllWatchesValue(getAllWatches().replace(',' + watch + ',', ',')
                       .replace(',' + watch, '')
                       .replace(watch + ',', ''))

def run(bot, chat_id, user='Dave', keyConfig=None, message='', totalResults=1):
    if not AllWatchesContains(chat_id):
        addToAllWatches(chat_id)
    topgifs = 'https://www.reddit.com/r/gifs/top.json'
    topgifsUrlRequest = urlfetch.fetch(url=topgifs, headers={'User-Agent': 'App Engine:Scenic-Oxygen:ImageBoet:v1.0 (by /u/SalamiArmy)'})
    data = json.loads(topgifsUrlRequest.content)
    top_gifs_walker(bot, chat_id, data)

def top_gifs_walker(bot, chat_id, data):
    offset = 0
    while int(offset) < 25:
        gif_url = data['data']['children'][offset]['data']['url']
        imagelink = gif_url[:-1] if gif_url.endswith('.gifv') else gif_url
        requestText = data['data']['children'][offset]['data']['title'].replace(' - Create, Discover and Share GIFs on Gfycat', '')# + ': https://www.reddit.com' + \
                      #data['data']['children'][offset]['data']['permalink']
        offset += 1
        if '?' in imagelink:
            imagelink = imagelink[:imagelink.index('?')]
        if not getgif.wasPreviouslySeenGif(chat_id, imagelink):
            getgif.addPreviouslySeenGifsValue(chat_id, imagelink)
            if getgif.is_valid_gif(imagelink):
                if retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, requestText):
                    break

