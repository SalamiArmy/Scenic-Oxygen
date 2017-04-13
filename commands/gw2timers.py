# coding=utf-8
import json
import urllib
import urllib2

from bs4 import BeautifulSoup


def run(bot, chat_id, user, keyConfig, message='', totalResults=1):
    steamGameLink = 'http://guildwarstemple.com/apps'
    html_code = urllib.urlopen(steamGameLink).read()
    gameResults = steam_game_parser(html_code).encode('utf-8')
    bot.sendMessage(chat_id=chat_id, text=gameResults,
                    disable_web_page_preview=True, parse_mode='Markdown')
    return True

def steam_game_parser(code):
    soup = BeautifulSoup(code, 'html.parser')
    AllEventDetailsFormatted = ''

    eventDiv = soup.find('div', attrs={'id':'ep1'})
    if eventDiv:
        namePane = soup.find('p', attrs={'class': 'event-name'})
        if namePane:
            AllEventDetailsFormatted += '*' + namePane.string + '*'
        else:
            raise Exception('Cannot parse event name for first event on timers page.')
    else:
        raise Exception('Cannot parse events from timers page.')

    descriptionDiv = soup.find('div', attrs={'class':'game_description_snippet'})
    if descriptionDiv:
        descriptionSnippet = descriptionDiv.string.replace('\r', '').replace('\n', '').replace('\t', '')
        AllEventDetailsFormatted += descriptionSnippet + '\n'
    else:
        raise Exception('Cannot parse description from Steam page for this game.')

    dateSpan = soup.find('span', attrs={'class':'date'})
    if dateSpan:
        releaseDate = dateSpan.string
        AllEventDetailsFormatted += 'Release Date: ' + releaseDate + '\n'
    else:
        raise Exception('Cannot parse release date from Steam page for this game.')

    featureList = ''
    featureLinks = soup.findAll('a', attrs={'class':'name'})
    if len(featureLinks) > 0:
        for featureLink in featureLinks:
            featureList += '     ' + featureLink.string.replace('Seated', 'Will make you shit yourself') + '\n'
        AllEventDetailsFormatted += 'Features:\n' + featureList

    reviewRows = ''
    reviewDivs = soup.findAll('div', attrs={'class':'user_reviews_summary_row'})
    if len(reviewDivs) > 0:
        for reviewRow in reviewDivs:
            reviewSubtitleDiv = reviewRow.find('div', attrs={'class':'subtitle column'}).string
            reviewSummaryDiv = reviewRow.find('div', attrs={'class':'summary column'}).string
            if not reviewSummaryDiv:
                reviewSummaryDiv = reviewRow.find('span', attrs={'class':'nonresponsive_hidden responsive_reviewdesc'}).string
            reviewSummaryDiv = reviewSummaryDiv.replace('\r', '').replace('\n', '').replace('\t', '')
            if reviewSummaryDiv != 'No user reviews':
                reviewRows += '     ' + reviewSubtitleDiv + reviewSummaryDiv.replace('-', '').replace(' user reviews', '').replace(' of the ', ' of ') + '\n'
        if reviewRows:
            AllEventDetailsFormatted += 'Reviews:\n' + reviewRows
        if AllEventDetailsFormatted.endswith('\n'):
            AllEventDetailsFormatted = AllEventDetailsFormatted[:AllEventDetailsFormatted.rfind('\n')]

    tagList = ''
    tagLinks = soup.findAll('a', attrs={'class':'app_tag'})
    if len(tagLinks) > 0:
        for tagLink in tagLinks:
            tagList += tagLink.string.replace('\r', '').replace('\n', '').replace('\t', '') + ', '
        AllEventDetailsFormatted += '\n' + 'Tags:\n`' + tagList
    if AllEventDetailsFormatted.endswith(', '):
        AllEventDetailsFormatted = AllEventDetailsFormatted[:AllEventDetailsFormatted.rfind(', ')]
        AllEventDetailsFormatted += '`'

    return AllEventDetailsFormatted