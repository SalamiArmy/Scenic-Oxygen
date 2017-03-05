# coding=utf-8
import urllib
import urllib2

from bs4 import BeautifulSoup


def run(bot, keyConfig, chat_id, user, message):
    requestText = message.replace(bot.name, '').strip()

    code = urllib.urlopen('http://www.acronymsearch.com/index.php?acronym=' + requestText).read()
    resultsList = acronym_results_parser(code)
    if resultsList:
        searchResults = acronym_results_printer(requestText, resultsList)
        bot.sendMessage(chat_id=chat_id, text=user + ', ' + searchResults,
                        disable_web_page_preview=True, parse_mode='Markdown')
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find the steam game ' + \
                                              requestText.encode('utf-8'))


def acronym_results_parser(code):
    soup = BeautifulSoup(code, 'html.parser')
    resultList = []
    for resultRow in soup.findAll('td', attrs={'width':'100%'}):
        resultList.append(resultRow.string)
    return resultList

def acronym_results_printer(request, list):
    AllGameDetailsFormatted= '*' + str(request).upper() + '* could mean:'
    for item in list:
        if (str(item) != 'None'):
            AllGameDetailsFormatted += '\n'
            for char in str(item)\
                    .rstrip('[military]')\
                    .rstrip('(insurance)')\
                    .rstrip('[transportation]')\
                    .rstrip('[computer]')\
                    .rstrip('(technology)')\
                    .rstrip('[medical]')\
                    .rstrip('[automotive]')\
                    .rstrip('[abbreviation]')\
                    .rstrip('[slang]'):
                if char.isupper():
                    AllGameDetailsFormatted += '*' + char + '*'
                else:
                    AllGameDetailsFormatted += char
    return AllGameDetailsFormatted