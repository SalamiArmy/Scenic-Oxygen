# coding=utf-8
import random

import soundcloud


def run(bot, keyConfig, chat_id, user, message, intention_confidence=0.0):
    requestText = message.replace(bot.name, "").strip()

    tracks = get_tracks(keyConfig, requestText)
    if len(tracks) >= 1:
        randint = random.randint(0, len(tracks) - 1)
        track_url = tracks[randint].permalink_url
        bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') + track_url +
                                              ('\nMight I add that I am ' + str(intention_confidence) + '% confident you wanted to hear this.' if intention_confidence > 0.0 else ''))
        return True
    else:
        if intention_confidence == 0.0:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find the sound of ' +
                                                  requestText.encode('utf-8') + '.')


def get_tracks(keyConfig, requestText):
    client = soundcloud.Client(client_id=keyConfig.get('Soundcloud', 'SC_CLIENT_ID'))
    tracks = client.get('/tracks', q=requestText.encode('utf-8'), sharing='public')
    return tracks
