# coding=utf-8
import ConfigParser
import json
import urllib

import telegram


def run(chat_id, user, message):
    # Read keys.ini file should be at program start (don't forget to put your keys in there!)
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

    requestText = message.replace(bot.name, "").strip()

    trackUrl = 'http://api.musixmatch.com/ws/1.1/track.search?apikey='
    data = json.load(urllib.urlopen(trackUrl + keyConfig.get('MusixMatch', 'APP_ID') + '&q=' + requestText))
    if 'message' in data and \
                    'body' in data['message'] and \
                    'track_list' in data['message']['body'] and \
                    len(data['message']['body']['track_list']) >= 1 and \
                    'track' in data['message']['body']['track_list'][0] and \
                    'artist_name' in data['message']['body']['track_list'][0]['track'] and \
                    'track_name' in data['message']['body']['track_list'][0]['track']:
        artist_name = data['message']['body']['track_list'][0]['track']['artist_name']
        track_name = data['message']['body']['track_list'][0]['track']['track_name']
        track_soundcloud_id = str(data['message']['body']['track_list'][0]['track']['track_soundcloud_id'])
        trackId = str(data['message']['body']['track_list'][0]['track']['track_id'])
        lyricsUrl = 'http://api.musixmatch.com/ws/1.1/track.lyrics.get?apikey='
        data = json.load(urllib.urlopen(lyricsUrl + keyConfig.get('MusixMatch', 'APP_ID') + '&track_id=' + trackId))
        lyrics_body = ''
        if 'message' in data and \
                        'body' in data['message'] and \
                        'lyrics' in data['message']['body'] and \
                        len(data['message']['body']['lyrics']) >= 1 and \
                        'lyrics_body' in data['message']['body']['lyrics']:
            lyrics_body = data['message']['body']['lyrics']['lyrics_body'].replace(
                '******* This Lyrics is NOT for Commercial use *******', '')
        bot.sendMessage(chat_id=chat_id, text=((user + ': ') if not user == '' else '') + track_name + ' by ' + artist_name + \
                                              ((
                                                   '\nListen at: https://api.soundcloud.com/tracks/' + track_soundcloud_id) if not track_soundcloud_id == '0' else '') + \
                                              (('\n' + lyrics_body) if not lyrics_body == '' else ''))
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find any tracks for the lyrics ' + \
                                              requestText.encode('utf-8'))