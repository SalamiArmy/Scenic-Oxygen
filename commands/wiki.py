# coding=utf-8
import json
import urllib


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()

    wikiUrl = \
        'https://simple.wikipedia.org/w/api.php?action=opensearch&limit=1&namespace=0&format=json&search='
    realUrl = wikiUrl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    total_sent = 0
    while int(total_sent) < len(data[2]) and int(total_sent) < int(totalResults):
        bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') +
                                              data[2][total_sent] + '\nLink: ' +
                                              data[3][total_sent].replace('https://simple.wikipedia.org',
                                                                          'https://en.wikipedia.org')
                        , disable_web_page_preview=True)
        total_sent += 1
    if int(total_sent) < int(totalResults):
        wikiUrl = \
            'https://en.wikipedia.org/w/api.php?action=opensearch&namespace=0&format=json&search='
        realUrl = wikiUrl + requestText.encode('utf-8')
        data = json.load(urllib.urlopen(realUrl))
        while int(total_sent) < len(data[2]) and int(total_sent) < int(totalResults):
            bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') +
                                                  data[2][total_sent] + '\nLink: ' + data[3][total_sent],
                            disable_web_page_preview=True)
            total_sent += 1
        if int(total_sent) < int(totalResults):
            bot.sendMessage(chat_id=chat_id,
                            text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                 ', I\'m afraid I can\'t find any wiki articles for ' +
                                 requestText.encode('utf-8') + '.')