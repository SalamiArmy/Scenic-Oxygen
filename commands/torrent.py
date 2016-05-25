# coding=utf-8
import ConfigParser
import os
import urllib

import telegram
#reverse image search imports:
import json


def run(thorin, update):
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(os.getenv("THORIN_API_TOKEN"))

    # chat_id is required to reply to any message
    chat_id = update.message.chat_id
    message = update.message.text
    user = update.message.from_user.username \
        if not update.message.from_user.username == '' \
        else update.message.from_user.first_name + (' ' + update.message.from_user.last_name) \
        if not update.message.from_user.last_name == '' \
        else ''

    message = message.replace(bot.name, "").strip()

    splitText = message.split(' ', 1)

    requestText = splitText[1] if ' ' in message else ''


    tor1Url = 'https://torrentproject.se/?s='
    searchUrl = tor1Url + requestText.encode('utf-8') + '&out=json'
    data = json.load(urllib.urlopen(searchUrl))
    torrageUrl = 'http://torrage.info/torrent.php?h='
    if data['total_found'] >= 1 and '1' in data:
        torrent = data['1']['torrent_hash']
        tTitle = data['1']['title']
        seeds = str(data['1']['seeds'])
        leechs = str(data['1']['leechs'])
        downloadUrl = torrageUrl + torrent.upper()
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'Torrent Name: ' + tTitle + \
                                  '\nDownload Link: ' + downloadUrl + \
                                  '\nSeeds: ' + seeds + \
                                  '\nLeechers: ' + leechs
        bot.sendMessage(chat_id=chat_id, text=urlForCurrentChatAction, disable_web_page_preview=True)
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I can\'t find any torrents for ' + \
                                  requestText.encode('utf-8') + '.'
        bot.sendMessage(chat_id=chat_id, text=urlForCurrentChatAction)