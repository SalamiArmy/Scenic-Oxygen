# coding=utf-8
import urllib
import urllib2

from bs4 import BeautifulSoup


def run(bot, keyConfig, chat_id, user, message=''):
    gameResults = get_steamcharts_top_games()
    if gameResults:
        bot.sendMessage(chat_id=chat_id, text=gameResults,
                        disable_web_page_preview=True, parse_mode='Markdown')
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find any popular steam games.')


def get_steamcharts_top_games():
    rawMarkup = urllib.urlopen('http://steamcharts.com/top').read()
    soup = BeautifulSoup(rawMarkup, 'html.parser')
    hot_games = '*Most Popular Steam Games:*'
    for resultRow in soup.findAll('td', attrs={'class':'game-name left'}):
        hot_games += '\n' + resultRow.text.replace('\n', '').replace('\t', '')
    return hot_games

def steam_game_name_parser(code, link):
    soup = BeautifulSoup(code, 'html.parser')

    titleDiv = soup.find('div', attrs={'class':'apphub_AppName'})
    if titleDiv:
        gameTitle = titleDiv.string
        return gameTitle
    else:
        return ''
