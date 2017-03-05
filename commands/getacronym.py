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
    AllGameDetailsFormatted= '*' + request + '* could mean:'
    for item in list:
        if (str(item) != 'None'):
            militarySuffix = '[military]'
            if (str(item).endswith(militarySuffix)):
                AllGameDetailsFormatted += '\n*' + str(item).rstrip(militarySuffix) + '*'
            insuranceSuffix = '(insurance)'
            if (str(item).endswith(insuranceSuffix)):
                AllGameDetailsFormatted += '\n_' + str(item).rstrip(insuranceSuffix) + '_'
            transportationSuffix = '[transportation]'
            if (str(item).endswith(transportationSuffix)):
                AllGameDetailsFormatted += '\n_' + str(item).rstrip(transportationSuffix) + '_'
            computerSuffix = '[computer]'
            if (str(item).endswith(computerSuffix)):
                AllGameDetailsFormatted += '\n`' + str(item).rstrip(computerSuffix) + '`'
            technologySuffix = '(technology)'
            if (str(item).endswith(technologySuffix)):
                AllGameDetailsFormatted += '\n`' + str(item).rstrip(technologySuffix) + '`'
            medicalSuffix = '[medical]'
            if (str(item).endswith(medicalSuffix)):
                AllGameDetailsFormatted += '\n_' + str(item).rstrip(medicalSuffix) + '_'
            automotiveSuffix = '[automotive]'
            if (str(item).endswith(automotiveSuffix)):
                AllGameDetailsFormatted += '\n_' + str(item).rstrip(automotiveSuffix) + '_'
            abbreviationSuffix = '[abbreviation]'
            if (str(item).endswith(abbreviationSuffix)):
                AllGameDetailsFormatted += '\n_' + str(item).rstrip(abbreviationSuffix) + '_'
            slangSuffix = '[slang]'
            if (str(item).endswith(slangSuffix)):
                AllGameDetailsFormatted += '\n_'
                for char in str(item).rstrip(slangSuffix):
                    if char.isupper():
                        AllGameDetailsFormatted += '*' + char + '*'
                    else:
                        AllGameDetailsFormatted += char
                AllGameDetailsFormatted += '_'
    return AllGameDetailsFormatted