# coding=utf-8
import json
import urllib
import urllib2


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, '').strip()

    url = 'https://api.cognitive.microsoft.com/bing/v5.0/suggestions/'
    values = {'q': requestText}

    data = urllib.urlencode(values)
    req = urllib2.Request(url + '?' + data)
    req.add_header('Ocp-Apim-Subscription-Key', keyConfig.get('Bing', 'AutoSuggestApiKey'))
    data = json.load(urllib2.urlopen(req))

    if 'suggestionGroups' in data and len(data['suggestionGroups']) >= 1 and 'searchSuggestions' in data['suggestionGroups'][0] and len(data['suggestionGroups'][0]['searchSuggestions']) >= 1 and 'displayText' in data['suggestionGroups'][0]['searchSuggestions'][0] and data['suggestionGroups'][0]['searchSuggestions'][0]['displayText'] != requestText:
        displayText = data['suggestionGroups'][0]['searchSuggestions'][0]['displayText']
        bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') + displayText)
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t find a suggestion for ' +
                                              requestText + '.')
