# coding=utf-8
import json
import urllib


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()

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
        bot.sendMessage(chat_id=chat_id, text='Torrent Name: ' + tTitle + \
                                              '\nDownload Link: ' + downloadUrl + \
                                              '\nSeeds: ' + seeds + \
                                              '\nLeechers: ' + leechs,
                        disable_web_page_preview=True)
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I can\'t find any torrents for ' + \
                                              requestText.encode('utf-8') + '.')