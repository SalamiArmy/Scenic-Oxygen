# coding=utf-8
import json
import urllib


def run(bot, keyConfig, chat_id, user, message):
    allMatchesUrl = 'http://cricscore-api.appspot.com/csa'
    getData = urllib.urlopen(allMatchesUrl).read().decode('utf-8')
    if ('<blockquote>' not in getData):
        allMatches = json.loads(getData)
        proteasMatchId = None
        for match in allMatches:
            if match['t1'] == 'South Africa' or match['t2'] == 'South Africa':
                proteasMatchId = match['id']
        if proteasMatchId == None:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid the Proteas are not playing right now.')
            return True
        else:
            matchesUrl = 'http://cricscore-api.appspot.com/csa?id=' + str(proteasMatchId)
            match = json.load(urllib.urlopen(matchesUrl))
            bot.sendMessage(chat_id=chat_id, text=(match[0]['si'] + '\n' + match[0]['de']))
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              getData[getData.index('<blockquote>') + len('<blockquote>'):getData.index('</blockquote>')]
                        .replace('<H1>', '*').replace('</H1>', '*').replace('<p>', ''), parse_mode='Markdown')
