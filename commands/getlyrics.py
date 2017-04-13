# coding=utf-8
import json
import urllib


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()

    trackUrl = 'http://api.musixmatch.com/ws/1.1/track.search?apikey='
    data = json.load(urllib.urlopen(trackUrl + keyConfig.get('MusixMatch', 'APP_ID') + '&q=' + requestText))
    if 'message' in data and \
                    'body' in data['message'] and \
                    'track_list' in data['message']['body'] and \
                    len(data['message']['body']['track_list']) >= 1 and \
                    'track' in data['message']['body']['track_list'][0] and \
                    'artist_name' in data['message']['body']['track_list'][0]['track'] and \
                    'track_name' in data['message']['body']['track_list'][0]['track'] and \
                    'track_id' in data['message']['body']['track_list'][0]['track']:
        artist_name = data['message']['body']['track_list'][0]['track']['artist_name']
        track_name = data['message']['body']['track_list'][0]['track']['track_name']
        if 'track_soundcloud_id' in data['message']['body']['track_list'][0]['track'] and str(data['message']['body']['track_list'][0]['track']['track_soundcloud_id']) != '':
            track_soundcloud_id = str(data['message']['body']['track_list'][0]['track']['track_soundcloud_id'])
        else:
            track_soundcloud_id = '0'
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
                '******* This Lyrics is NOT for Commercial use *******\n(1409612423371)', '')
        bot.sendMessage(chat_id=chat_id, text=((user + ': ') if not user == '' else '') + track_name + ' by ' + artist_name + \
                                              ((
                                                   '\nListen at: https://api.soundcloud.com/tracks/' + track_soundcloud_id) if not track_soundcloud_id == '0' else '') + \
                                              (('\n' + lyrics_body) if not lyrics_body == '' else ''))
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find any tracks for the lyrics ' + \
                                              requestText.encode('utf-8'))