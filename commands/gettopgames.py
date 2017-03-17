# coding=utf-8
import urllib
import urllib2

from bs4 import BeautifulSoup


def run(bot, keyConfig, chat_id, user, message=''):
    gameResults = get_steam_top_games()
    if gameResults:
        bot.sendMessage(chat_id=chat_id, text=gameResults,
                        disable_web_page_preview=True, parse_mode='Markdown')
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find any hot steam games.')


def get_steam_top_games():
    rawMarkup = urllib.urlopen('http://store.steampowered.com/search/?filter=topsellers').read()
    soup = BeautifulSoup(rawMarkup, 'html.parser')
    resultList = []
    for resultRow in soup.findAll('a', attrs={'class':'search_result_row'}):
        if 'data-ds-appid' in resultRow.attrs:
            resultList.append(resultRow['data-ds-appid'])
        if 'data-ds-bundleid' in resultRow.attrs:
            resultList.append(resultRow['data-ds-bundleid'])
    resultsListLength = len(resultList)
    hot_games = '*Top Steam Games:*'
    if resultsListLength > 0:
        SearchResultsInterator = 0
        while (SearchResultsInterator<resultsListLength):
            steamGameLink = 'http://store.steampowered.com/app/' + resultList[SearchResultsInterator]
            bypassAgeGate = urllib2.build_opener()
            bypassAgeGate.addheaders.append(('Cookie', 'birthtime=578390401'))
            code = bypassAgeGate.open(steamGameLink).read()
            game_name = steam_game_name_parser(code, steamGameLink)
            if game_name:
                hot_games += '\n' + game_name
            SearchResultsInterator += 1
    return hot_games

def steam_game_name_parser(code, link):
    soup = BeautifulSoup(code, 'html.parser')

    titleDiv = soup.find('div', attrs={'class':'apphub_AppName'})
    if titleDiv:
        gameTitle = titleDiv.string
        return gameTitle
    else:
        return ''
