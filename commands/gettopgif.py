# coding=utf-8
import json
import urllib2

from commands import retry_on_telegram_error
from commands import getgif


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    topgifs = 'https://www.reddit.com/r/gifs/top.json'
    topgifsUrlRequest = urllib2.Request(topgifs, headers={'User-Agent': "Magic Browser"})
    data = json.load(urllib2.urlopen(topgifsUrlRequest))
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

