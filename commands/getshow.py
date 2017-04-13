# coding=utf-8
import json
import re
import urllib

import telegram


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()


    showsUrl = 'http://api.tvmaze.com/search/shows?q='
    data = json.load(urllib.urlopen(showsUrl + requestText))
    if len(data) >= 1:
        formattedShowSnippet = re.sub(r'<[^>]*?>', '',
                                      data[0]['show']['summary']
                                       .replace('<span class="searchmatch">', '*')
                                       .replace('</span>', '*')
                                       .replace('&quot;', '\"')
                                       .replace('[', '')
                                       .replace(']', '')
                                       .replace('\\', '')[:125].strip())
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        image_original = data[0]['show']['image']['original'].encode('utf-8')
        bot.sendPhoto(chat_id=chat_id,
                      photo=image_original,
                      caption=formattedShowSnippet)
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I cannot find the TV show ' + \
                                              requestText.title())