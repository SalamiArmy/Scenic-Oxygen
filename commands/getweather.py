# coding=utf-8
import ConfigParser
import os
import urllib
import json


def run(bot, keyConfig, chat_id, user, message):
    requestText = message.replace(bot.name, "").strip()


    yahoourl = \
        "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20" \
        "in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%27" + requestText.encode(
            'utf-8') + "%27)%20" \
                       "and%20u%3D%27c%27&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
    result = urllib.urlopen(yahoourl).read()
    data = json.loads(result)
    if data['query']['count'] == 1:
        weather = data['query']['results']['channel']['item']['condition']
        forecast = data['query']['results']['channel']['item']['forecast']
        city = data['query']['results']['channel']['location']['city']
        astronomy = data['query']['results']['channel']['astronomy']
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = ('It is currently ' + weather['text'] + ' in ' + city +
                                   ' with a temperature of ' + weather['temp'] + 'C.\nA high of ' +
                                   forecast[0]['high'] + ' and a low of ' + forecast[0]['low'] +
                                   ' are expected during the day with conditions being ' +
                                   forecast[0]['text'] + '.\nSunrise: ' + astronomy['sunrise'] +
                                   '\nSunset: ' + astronomy['sunset'])
        bot.sendMessage(chat_id=userWithCurrentChatAction,
                        text=urlForCurrentChatAction,
                        parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I don\'t know the place ' + \
                                  requestText.encode('utf-8') + '.'
        bot.sendMessage(chat_id=chat_id, text=urlForCurrentChatAction)