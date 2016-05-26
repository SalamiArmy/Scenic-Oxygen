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

    allMatchesUrl = 'http://cricscore-api.appspot.com/csa'
    allMatches = json.load(urllib.urlopen(allMatchesUrl))
    proteasMatchId = None
    for match in allMatches:
        if match['t1'] == 'South Africa' or match['t2'] == 'South Africa':
            proteasMatchId = match['id']
    if proteasMatchId == None:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid the Proteas are not playing right now.')
    else:
        matchesUrl = 'http://cricscore-api.appspot.com/csa?id=' + str(proteasMatchId)
        match = json.load(urllib.urlopen(matchesUrl))
        bot.sendMessage(chat_id=chat_id, text=(match[0]['si'] + '\n' + match[0]['de']))