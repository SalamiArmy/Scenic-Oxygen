# coding=utf-8
import json
import urllib


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    vidurl = 'https://www.googleapis.com/youtube/v3/search?safeSearch=none&type=video&key=' + \
             keyConfig.get('Google', 'GCSE_APP_ID') + '&part=snippet&q='
    realUrl = vidurl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    if 'items' in data and len(data['items']) >= 1:
        vidlink = data['items'][0]['id']['videoId']
        bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') +
                                              'https://www.youtube.com/watch?v=' + vidlink + '&type=video')
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t do that.\n(Video not found)')